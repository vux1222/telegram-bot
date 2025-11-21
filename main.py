import logging
import hashlib
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# ================= CẤU HÌNH =================
# Token của bạn
BOT_TOKEN = "8344403257:AAF0F3V3A29RLr6T1Rd9ZHdtTzby0IO67fM"
# ============================================

# Thiết lập ghi log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- CÔNG THỨC TÍNH KEY ---
def calculate_vip_key(device_id, username):
    try:
        # Lấy ngày hiện tại định dạng yyyyMMdd
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        
        # Ghép chuỗi: MãThiếtBị + TênUser + Ngày
        raw_data = f"{device_id}{username}{today_str}"
        
        # Mã hóa SHA1
        sha1_hash = hashlib.sha1(raw_data.encode('utf-8')).hexdigest()
        
        # Lấy 6 ký tự đầu và viết hoa
        return sha1_hash[:6].upper()
    except Exception as e:
        return "ERROR"

# --- CÁC LỆNH CỦA BOT ---

# 1. Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Xin chào! Tôi là Bot cấp mật khẩu.**\n\n"
        "📖 **Cách dùng siêu nhanh:**\n"
        "👉 Chỉ cần nhắn **Mã Thiết Bị** vào đây, tôi sẽ gửi mật khẩu!\n"
        "Ví dụ nhắn: `ABC314A`",
        parse_mode='Markdown'
    )

# 2. Hàm xử lý tin nhắn thường (Nhập mã máy trực tiếp)
async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Lấy nội dung tin nhắn người dùng gửi
        device_id = update.message.text.strip()
        
        # User mặc định
        username = "123"

        # Tính toán Key
        key_result = calculate_vip_key(device_id, username)
        
        # Lấy ngày hiện tại để hiển thị
        display_date = datetime.datetime.now().strftime("%d/%m/%Y")

        # Trả lời
        response_msg = (
            f"🔐 **THÀNH CÔNG**\n"
            f"----------------------\n"
            f"💻 Mã máy: `{device_id}`\n"
            f"👤 User: `{username}`\n"
            f"🔑 **MẬT MÃ:** `{key_result}`\n\n"
            f"_(Ngày: {display_date})_\n\n"
            f"©By Nong Van Vu"
        )
        
        # Reply lại tin nhắn của người dùng
        await update.message.reply_text(response_msg, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi: {e}")

# 3. Lệnh /key cũ (Giữ lại để dùng nếu muốn nhập User khác)
async def get_key_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
             await update.message.reply_text("⚠️ Dùng lệnh này để nhập User khác:\n`/key <MãMáy> <User>`", parse_mode='Markdown')
             return
        
        device_id = args[0]
        username = args[1]
        key_result = calculate_vip_key(device_id, username)
        display_date = datetime.datetime.now().strftime("%d/%m/%Y")
        
        response_msg = (
            f"🔐 **KEY (User Tùy Chọn)**\n"
            f"----------------------\n"
            f"💻 Mã máy: `{device_id}`\n"
            f"👤 User: `{username}`\n"
            f"🔑 **MẬT MÃ:** `{key_result}`\n\n"
            f"_(Ngày: {display_date})_\n\n"
            f"©By Nong Van Vu"
        )
        await update.message.reply_text(response_msg, parse_mode='Markdown')
    except Exception:
        pass

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == '__main__':
    print("🚀 Đang khởi động Boss Tele...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Đăng ký lệnh /start
    app.add_handler(CommandHandler("start", start))
    
    # Đăng ký lệnh /key (cho trường hợp muốn nhập user khác)
    app.add_handler(CommandHandler("key", get_key_command))
    
    # Đăng ký xử lý tin nhắn văn bản (QUAN TRỌNG: Để cái này cuối cùng)
    # Nó sẽ bắt tất cả tin nhắn KHÔNG PHẢI là lệnh
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    print("✅ Boss đã online! (Chế độ: Nhắn mã máy là có Key)")

    app.run_polling()
