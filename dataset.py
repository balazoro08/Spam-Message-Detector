"""
Dataset module for Spam Message Detector.
Provides a comprehensive multi-domain (SMS, Email, Comments) dataset
with labeled spam and ham (legitimate) messages.
"""

# Rich multi-domain dataset covering SMS, Email, and Social Media/Blog Comments
DATASET_SAMPLES = [
    # --- SMS SPAM ---
    {"text": "URGENT! You have won a $1,000 Walmart Gift Card. Click http://bit.ly/claim-card now to claim your prize! Reply STOP to optout", "channel": "sms", "label": 1},
    {"text": "Congratulations! Your phone number was selected as today's $500 winner. Call 0800 123 4567 immediately to claim.", "channel": "sms", "label": 1},
    {"text": "ALERT: Your Bank account has been compromised! Please verify your password at http://secure-bank-login-verify.com immediately.", "channel": "sms", "label": 1},
    {"text": "HOT SINGLE CHATS! Text DATE to 88010 to connect with locals near you now! £1.50 per msg.", "channel": "sms", "label": 1},
    {"text": "FINAL NOTICE: Your package delivery failed due to unpaid shipping fee of $2.99. Pay now at http://usps-tracking-redelivery.org", "channel": "sms", "label": 1},
    {"text": "You have 1 new unread photo message! View here: http://get-pic-now.net/msg3921. Charges apply.", "channel": "sms", "label": 1},
    {"text": "Free entry in a £1000 cash draw! Text WIN to 80082. Terms apply. 18+ only.", "channel": "sms", "label": 1},
    {"text": "Loan approved instantly up to $50,000 with NO credit check! Apply at http://quick-cash-now.co", "channel": "sms", "label": 1},
    {"text": "CLAIM YOUR FREE iPhone 15 Pro Max! Only 3 left in stock. Click link: http://apple-reward-claim.com", "channel": "sms", "label": 1},
    {"text": "Your tax refund of $1,420 is pending approval. Submit your SSN and details here: http://irs-refund-portal.net", "channel": "sms", "label": 1},
    {"text": "Urgent Security Code: Someone logged into your Account from Russia. Click http://auth-alert-check.com to secure your account.", "channel": "sms", "label": 1},
    {"text": "Earn $500/day working from home 2 hours daily! No experience required. WhatsApp +1-555-0199 now!", "channel": "sms", "label": 1},
    {"text": "Exclusive offer: 80% OFF Ray-Ban Sunglasses! Limited time sale. Shop now at http://cheap-sunglasses-sale.online", "channel": "sms", "label": 1},
    {"text": "Your mobile subscription renewal is due. $49.99 will be charged automatically unless you cancel at http://cancel-sub.me", "channel": "sms", "label": 1},

    # --- SMS HAM (LEGITIMATE) ---
    {"text": "Hey Alex, are we still meeting for lunch at 12:30 PM at the diner?", "channel": "sms", "label": 0},
    {"text": "Your verification code for Google is 482019. Do not share this code with anyone.", "channel": "sms", "label": 0},
    {"text": "Hi Mom, just got home safely from the trip. Talk to you tomorrow morning!", "channel": "sms", "label": 0},
    {"text": "Reminder: Your dental appointment is scheduled for tomorrow at 3:00 PM with Dr. Smith.", "channel": "sms", "label": 0},
    {"text": "Can you please send me the project report PDF when you get a chance?", "channel": "sms", "label": 0},
    {"text": "Your Uber driver David is arriving in a Silver Toyota Camry (Plate: 7ABC123).", "channel": "sms", "label": 0},
    {"text": "Thanks for dinner last night! Had a really great time catching up with everyone.", "channel": "sms", "label": 0},
    {"text": "Your Amazon package with tracking #9400111234 has been delivered to your front porch.", "channel": "sms", "label": 0},
    {"text": "Hey, running about 10 minutes late due to traffic. See you guys soon!", "channel": "sms", "label": 0},
    {"text": "Don't forget to bring your passport and boarding pass for our flight tomorrow.", "channel": "sms", "label": 0},
    {"text": "The grocery list: milk, eggs, whole wheat bread, and apples. Thank you!", "channel": "sms", "label": 0},
    {"text": "Your prescription #49281 is ready for pickup at CVS Pharmacy on Main St.", "channel": "sms", "label": 0},
    {"text": "Hey, did you watch the match yesterday? That final goal was unbelievable!", "channel": "sms", "label": 0},

    # --- EMAIL SPAM ---
    {
        "text": "Subject: URGENT: Inheritance Transfer of $14.5 Million USD\nDear Friend, I am Mr. Abacha writing to seek your assistance in transferring $14,500,000 from a dormant bank account. Reply immediately with your full name, bank details, and copy of passport.",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: Account Suspended - Action Required Immediately\nYour PayPal account has been temporarily restricted due to suspicious login attempts. Verify your credit card information within 24 hours at http://paypal-security-verification-update.com or your account will be permanently closed.",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: Make $10,000 per week from your living room!\nDiscover the secret automated Crypto Trading Bot that guarantees 300% daily returns! Zero risk, instant payouts directly to your wallet. Click here to get started today: http://crypto-wealth-matrix.io",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: VIAGRA / CIALIS 75% OFF - Fast Anonymous Shipping\nBuy top quality prescription medicines online without prescription! Guaranteed overnight delivery. Order today at http://pharma-direct-discount.pharmacy",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: Congratulations! You were pre-approved for a $250,000 business loan!\nNo collateral required, bad credit accepted. Money in your bank account in 24 hours. Fill out your application at http://express-funding-loans.net",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: RE: Unclaimed Lottery Winnings Notice\nOfficial Notification: Your email address won £850,000 in the UK National Lottery. To process your claim, contact our claims officer at claims@lottery-payouts-uk.com with your address.",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: Invoice Overdue - Immediate Payment Required\nAttached is invoice #98241 for $4,980.00. Failure to pay within 48 hours will result in legal action and credit reporting. Click http://invoice-payment-gateway-secure.org to clear balance.",
        "channel": "email",
        "label": 1
    },
    {
        "text": "Subject: Double your Bitcoin in 1 Hour!\nSend 0.05 BTC to wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and receive 0.10 BTC back immediately! Verified promotion by Elon Musk.",
        "channel": "email",
        "label": 1
    },

    # --- EMAIL HAM (LEGITIMATE) ---
    {
        "text": "Subject: Q3 Financial Performance Review & Strategy Meeting Agenda\nHi Team, Attached is the draft agenda for our Q3 review scheduled for Thursday at 10 AM EST. Please review the revenue figures and bring your department updates.",
        "channel": "email",
        "label": 0
    },
    {
        "text": "Subject: Your Order Confirmation - Order #112-98401-29401\nThank you for your order with TechStore! We are preparing your items for shipment. Estimated delivery date: Oct 8, 2026. View your order details in your account dashboard.",
        "channel": "email",
        "label": 0
    },
    {
        "text": "Subject: Project Update: Q4 Design System Sprint\nHello everyone, We completed the dark mode component tokens today. You can inspect the Figma file and pull the updated CSS variables from the main branch.",
        "channel": "email",
        "label": 0
    },
    {
        "text": "Subject: Flight Itinerary - San Francisco to New York\nYour flight booking is confirmed. Confirmation Code: K8X9P2. Flight UA412 departs SFO at 8:15 AM on Monday. Check-in opens 24 hours prior to departure.",
        "channel": "email",
        "label": 0
    },
    {
        "text": "Subject: Weekly Engineering Newsletter - Issue #42\nIn this week's issue: Best practices for Python 3.13 performance optimization, microservices architecture patterns, and our top community blog posts.",
        "channel": "email",
        "label": 0
    },
    {
        "text": "Subject: Inquiry regarding Software Engineer application\nDear Hiring Team, Thank you for taking the time to interview me yesterday. I enjoyed learning more about the platform engineering team and wanted to reiterate my interest in the position.",
        "channel": "email",
        "label": 0
    },
    {
        "text": "Subject: Monthly Utility Statement - Electric & Gas\nYour monthly statement for September is ready. Total amount due: $84.20 by Oct 20. Auto-pay is enabled for this account.",
        "channel": "email",
        "label": 0
    },

    # --- COMMENTS SPAM ---
    {"text": "Great post! Check out my profile to get 10,000 real Instagram followers for free in 5 minutes! http://insta-boost-followers.tk", "channel": "comment", "label": 1},
    {"text": "I made $15,000 in one month trading forex thanks to Mrs. Sarah! Contact her on WhatsApp +1-987-654-3210 for guaranteed signals!", "channel": "comment", "label": 1},
    {"text": "BUY CHEAP XANAX VALIUM OXYCONTIN WITHOUT PRESCRIPTION FAST SHIPPING CLICK HERE >>> http://meds-online-discount.ru", "channel": "comment", "label": 1},
    {"text": "Earn money online with zero investment! Just visit http://work-from-home-daily-cash.net and start earning $200 per hour!", "channel": "comment", "label": 1},
    {"text": "Sub4Sub? Subscribe to my YouTube channel and I will subscribe back to yours instantly! Let's grow together!", "channel": "comment", "label": 1},
    {"text": "Telegram link for leaked crypto pumps: t.me/crypto_insider_signals_100x Join now before it gets private!", "channel": "comment", "label": 1},
    {"text": "KPOP Merch 90% Discount clearance sale! Free worldwide shipping http://kpop-album-cheap-sale.com", "channel": "comment", "label": 1},
    {"text": "Want to recover your hacked Instagram or Facebook account? DM Mr. Cyber_Expert on Telegram @hacker_pro_tools", "channel": "comment", "label": 1},

    # --- COMMENTS HAM (LEGITIMATE) ---
    {"text": "This explanation was super clear and helpful! Loved how you broke down the NLP preprocessing steps.", "channel": "comment", "label": 0},
    {"text": "Does this approach work with newer versions of scikit-learn? I ran into a minor deprecation warning on line 42.", "channel": "comment", "label": 0},
    {"text": "Great tutorial! Could you make a follow-up video explaining how to deploy this model to AWS or Docker?", "channel": "comment", "label": 0},
    {"text": "I really agree with your point about feature engineering being more important than hyperparameter tuning here.", "channel": "comment", "label": 0},
    {"text": "Thanks for sharing the code repository! Starred it on GitHub.", "channel": "comment", "label": 0},
    {"text": "What dataset did you use for training? Is it publicly available on Kaggle or Hugging Face?", "channel": "comment", "label": 0},
    {"text": "Awesome project! The UI design is super sleek and dark mode looks incredible.", "channel": "comment", "label": 0},
]

def get_raw_dataset():
    """Returns the list of dataset samples."""
    return DATASET_SAMPLES
