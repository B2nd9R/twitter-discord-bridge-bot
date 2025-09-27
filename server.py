from fastapi import FastAPI
import os
import asyncio
from main import TwitterDiscordBot, load_config, setup_logging, logger

app = FastAPI()
bot_instance = None

@app.on_event("startup")
async def startup_event():
    global bot_instance
    # تحميل الإعدادات
    config = load_config()
    setup_logging(config.log_level, config.data_dir)
    
    # إنشاء البوت وتشغيله كـ task
    bot_instance = TwitterDiscordBot(config)
    asyncio.create_task(bot_instance.run())
    logger.info("بوت Twitter-Discord يعمل في الخلفية")

@app.get("/")
async def health_check():
    """للتأكد من أن الخدمة تعمل"""
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
