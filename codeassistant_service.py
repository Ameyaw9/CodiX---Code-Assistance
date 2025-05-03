import grpc
from concurrent import futures
import codeassistant_pb2
import codeassistant_pb2_grpc
import httpx
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

class CodeAssistantService(codeassistant_pb2_grpc.codeassistantServicer):

    def AskQuestion(self, request, context):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            answer = loop.run_until_complete(self._async_answer(request.question, request.context))
            loop.close()
            return codeassistant_pb2.AnswerResponse(answer=answer, success=True)
        except Exception as e:
            logging.error(f"Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return codeassistant_pb2.AnswerResponse(answer="", success=False)

    async def _async_answer(self, question, context):
        async with httpx.AsyncClient() as client:
            payload = {"question": question, "context": context}
            logging.info(f"Sending: {payload}")
            response = await client.post("https://my.api/endpoint", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("answer", "No response")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    codeassistant_pb2_grpc.add_codeassistantServicer_to_server(CodeAssistantService(), server)
    server.add_insecure_port('[::]:7861')
    server.start()
    logging.info("CodeAssistant server running on port 7861")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
