import logging
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration and Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Mock Data for Nairobi Matatu Routes
# In a real scenario, this would come from an API or database
MATATU_DATA = {
    "111": {"to": "Ngong", "boarding": "Railways", "fare_peak": 100, "fare_off": 70},
    "125": {"to": "Rongai", "boarding": "Railways", "fare_peak": 120, "fare_off": 80},
    "126": {"to": "Rongai (Kiserian)", "boarding": "Railways", "fare_peak": 150, "fare_off": 100},
    "46": {"to": "Kawangware", "boarding": "Kencom/Ambassadeur", "fare_peak": 50, "fare_off": 30},
    "102": {"to": "Dagoretti", "boarding": "Kencom", "fare_peak": 80, "fare_off": 50},
    "23": {"to": "Outer Ring/Kayole", "boarding": "Odeon/Commercial", "fare_peak": 80, "fare_off": 50},
    "44": {"to": "Kasarani", "boarding": "BS/Tuskys", "fare_peak": 80, "fare_off": 50},
    "100": {"to": "Kiambu", "boarding": "Old Nation", "fare_peak": 70, "fare_off": 50},
    "58": {"to": "Buruburu", "boarding": "Ambassadeur", "fare_peak": 70, "fare_off": 40}
}

def get_current_fare_type():
    """Determines if it is currently peak hour in Nairobi (simple logic)."""
    now = datetime.datetime.now().hour
    # Peak hours: 6-9 AM and 4-8 PM
    if (6 <= now <= 9) or (16 <= now <= 20):
        return "fare_peak", "Peak Hour 🚨"
    return "fare_off", "Off-Peak 🟢"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message and command instructions."""
    user = update.effective_user
    message = (
        f"Jambo {user.first_name}! 🚌\n"
        "Welcome to the Nairobi Matatu Route Bot (2026 Edition).\n\n"
        "Available Commands:\n"
        "/routes - View common matatu routes\n"
        "/fare <number> - Get fare info for a specific route\n"
        "/search <place> - Search routes by destination name\n"
        "/help - Show this manual"
    )
    await update.message.reply_text(message)

async def list_routes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lists all available routes in the mock database."""
    output = "📍 Available Matatu Routes:\n\n"
    for route, info in MATATU_DATA.items():
        output += f"• *{route}*: To {info['to']}\n"
    await update.message.reply_text(output, parse_mode='Markdown')

async def get_fare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches specific fare and boarding info for a route number."""
    if not context.args:
        await update.message.reply_text("Usage: /fare 111")
        return
    
    route_id = context.args[0]
    if route_id in MATATU_DATA:
        data = MATATU_DATA[route_id]
        fare_key, status = get_current_fare_type()
        fare_amount = data[fare_key]
        
        response = (
            f"🚍 *Route {route_id}*\n"
            f"Target: {data['to']}\n"
            f"Boarding Point: {data['boarding']}\n"
            f"Current Status: {status}\n"
            f"Estimated Fare: *KES {fare_amount}*\n\n"
            f"Note: Prices fluctuate based on weather and traffic."
        )
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Route not found. Try /routes to see the list.")

async def search_route(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Searches for a route by destination name substring."""
    if not context.args:
        await update.message.reply_text("Usage: /search Ngong")
        return
    
    query = " ".join(context.args).lower()
    results = []
    for rid, info in MATATU_DATA.items():
        if query in info['to'].lower():
            results.append(f"{rid} to {info['to']}")
    
    if results:
        await update.message.reply_text("🔎 Found matching routes:\n" + "\n".join(results))
    else:
        await update.message.reply_text("😔 No routes found matching that destination.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fallback for unknown commands."""
    await update.message.reply_text("I didn't understand that. Try /start for valid commands.")

def main():
    """Entry point for the bot."""
    # Replace with your actual Bot Token from @BotFather
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    application = Application.builder().token(TOKEN).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("routes", list_routes))
    application.add_handler(CommandHandler("fare", get_fare))
    application.add_handler(CommandHandler("search", search_route))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), unknown))

    print("Matatu Bot 2026 is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()