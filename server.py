#!/usr/bin/env python3
"""Optional AI companion backend, serves frontend and proxies responses."""
import os,json,urllib.request,urllib.error
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def respond(self,code,obj):
  data=json.dumps(obj,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.send_header('Access-Control-Allow-Origin','same-origin');self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if self.path=='/api/health':return self.respond(200,{'ok':True,'configured':bool(os.environ.get('OPENAI_API_KEY'))})
  return super().do_GET()
 def do_POST(self):
  if self.path!='/api/chat':return self.respond(404,{'error':'not found'})
  key=os.environ.get('OPENAI_API_KEY','')
  if not key:return self.respond(503,{'error':'服务端尚未设置 OPENAI_API_KEY'})
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n<1 or n>10000:return self.respond(413,{'error':'请求过大'})
   data=json.loads(self.rfile.read(n));q=data.get('question','')
   if not isinstance(q,str) or not 1<=len(q.strip())<=1200:return self.respond(400,{'error':'请提供不超过 1200 字的科学问题'})
   body={'model':os.environ.get('OPENAI_MODEL','gpt-4.1-mini'),'messages':[{'role':'system','content':'你是严谨、通俗的中文科学老师。区分科学事实、模型假设和不确定性。不要杜撰实验数据。优先解释科学原理，给出安全、可操作的小实验。回答尽量在500字以内。'},{'role':'user','content':q}],'temperature':0.5,'max_tokens':900}
   api=os.environ.get('OPENAI_BASE_URL','https://api.openai.com/v1').rstrip('/')+'/chat/completions'
   req=urllib.request.Request(api,data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
   with urllib.request.urlopen(req,timeout=22) as resp:out=json.load(resp)
   answer=out['choices'][0]['message']['content'];return self.respond(200,{'answer':answer})
  except urllib.error.HTTPError as e:return self.respond(502,{'error':'AI 上游服务请求失败（HTTP '+str(e.code)+'）'})
  except Exception:return self.respond(502,{'error':'AI 请求超时或返回异常，请检查服务端网络与模型配置'})
if __name__=='__main__':
 port=int(os.environ.get('PORT','8000'));print('Listening on',port);ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
