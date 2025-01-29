import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import grpc
from grpc.aio import ServicerContext
from mahakala_proto.gen.python.order.order_pb2_grpc import add_OrderServicer_to_server, OrderServicer
from mahakala_proto.gen.python.order.order_pb2 import OrderResponse, OrderRequest
from app.botkit.user_router import user_router

load_dotenv()


dp = Dispatcher()
dp.include_routers(user_router)
class OrderServiceImp(OrderServicer):
    def __init__(self, bot: Bot):
        self.bot = bot  

    async def TelegramOrder(self, request: OrderRequest, context: ServicerContext):
        print(f"Received order_id: {request}")
        message_text = f"Новый заказ: {request}"
        await self.bot.send_message(chat_id=1195173283, text=message_text)
        return OrderResponse(ok ="true")

# Асинхронная функция для старта gRPC сервера
async def grpc_server(bot: Bot):
    server = grpc.aio.server()
    order_service = OrderServiceImp(bot)  # Передаем бот в сервис
    add_OrderServicer_to_server(order_service, server)
    address = f"{os.getenv("HOST")}:{os.getenv("PORT")}"
    server.add_insecure_port(address)
    print(f"gRPC server started on {address}")
    await server.start()
    await server.wait_for_termination()

# Асинхронная функция для старта всех сервисов
async def start_services():
   
    bot = Bot(token=os.getenv("TOKEN"))
    await bot.delete_webhook(drop_pending_updates=True)
    
  
    grpc_task = asyncio.create_task(grpc_server(bot))  
    bot_task = asyncio.create_task(dp.start_polling(bot))  

    await grpc_task
    await bot_task

# Запуск всех сервисов
if __name__ == "__main__":
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("Бот выключен")
