import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import grpc
from grpc.aio import ServicerContext
from mahakala_proto.gen.python.order.order_pb2_grpc import add_OrderServicer_to_server, OrderServicer
from mahakala_proto.gen.python.order.order_pb2 import OrderResponse, OrderRequest
from aiogram.types import FSInputFile
from botkit.user_router import user_router
from excel.createExcel import createExcelOrder
load_dotenv()


dp = Dispatcher()
dp.include_routers(user_router)
class OrderServiceImp(OrderServicer):
    def __init__(self, bot: Bot):
        self.bot = bot
      
    def create_tabel_users(self,order:OrderRequest):
        self.order = createExcelOrder(orderlist=order,filename='users.xlsx')
    
    async def TelegramOrder(self, request: OrderRequest, context: ServicerContext):
        print(f"Received order_id: {request}")
        message_text = f"Новый заказ: {request}"
        chat_id=os.getenv("CHAT_ID")
        file = FSInputFile("excel_files/users.xlsx")
        self.create_tabel_users(request)


        await self.bot.send_document(chat_id=chat_id, document=file,caption="Вот ваш заказ 📄")
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
    try:
        await server.wait_for_termination()
    finally:
        await server.stop(grace=3)


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
    except asyncio.CancelledError:
        print("Сервисы остановлены")
    except KeyboardInterrupt:
        print("Бот выключен")
