import grpc
import codeassistant_pb2
import codeassistant_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:7861')
    stub = codeassistant_pb2_grpc.codeassistantStub(channel)

    print("Ask CodeAssistant a question (type 'exit' to quit):\n")

    while True:
        question = input("You: ")
        if question.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        context = input("Context (optional): ")

        try:
            request = codeassistant_pb2.QuestionRequest(question=question, context=context)
            response = stub.AskQuestion(request, timeout=60)
            print("CodeAssistant:", response.answer)
        except grpc.RpcError as e:
            print(f"gRPC Error: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
