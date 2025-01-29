import os
from aiogram import Bot,Dispatcher
from dotenv import load_dotenv
import grpc
from mahakala_proto.gen.python.order.order_pb2_grpc import add_OrderServicer_to_server,OrderServicer
from mahakala_proto.gen.python.order.order_pb2 import OrderResponse


load_dotenv()

bot = Bot(token = os.getenv("TOKEN"))
dp = Dispatcher()

class OrderServiceImp(OrderServicer):
    async def TelegramOrder(self, request, context):
        print(f"hello world: {request}")
        
        return OrderResponse(success=True, message=f"Order {request.order_id} processed successfully")
       
       

async def grpc_server():
    server = grpc.aio.server()
    add_OrderServicer_to_server(OrderServiceImp(), server)
    address = "localhost:50051"
    print(f"gRPC server started on {address}")
    server.add_insecure_port(address)
    await server.start()
    await server.wait_for_termination()


async def start_services():
    grpc_task = asyncio.create_task(grpc_server())
    bot_task = asyncio.create_task(main())
    
    await grpc_task
    await bot_task

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ =="__main__":
    import asyncio
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("бот выключен")
    