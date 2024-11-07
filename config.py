import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

UNRELATED_RESPONSES = [
    "I’m here to assist with portfolio optimization. 📊 Let’s focus on that!",
    "This doesn’t seem related to portfolio optimization. 💼 How can I help with your projects?",
    "For now, I’m focused on portfolio optimization. Let me know if you need assistance. 📈",
    "My expertise is in portfolio optimization. 📋 Do you have questions on that?",
    "Let’s stay on the topic of portfolio optimization. 📊 How can I assist?",
    "I’m here to support with portfolio management and optimization. 💡",
    "I specialize in portfolio optimization. 💼 How can I assist in that area?",
    "It seems we may be off-topic. Would you like to discuss portfolio optimization? 📈",
    "I’m here to help with optimizing your project portfolio. 🔍 Let me know how I can support you!",
    "My role is to assist with portfolio optimization. 📊 How can I help with that?",
    "This appears unrelated to portfolio optimization. 📋 Let me know if I can assist with that!",
    "Let’s keep our focus on portfolio optimization. 📈 How can I support your goals?",
    "Portfolio optimization is my primary function. 💼 Do you have questions on that?",
    "I’m equipped to help with portfolio optimization tasks. Shall we proceed? 📊",
    "My focus is portfolio optimization. 📈 Let me know if you’d like assistance there.",
    "It looks like we may be off track. Do you have portfolio-related questions? 📊",
    "I’m here for portfolio optimization support. 💼 How can I assist with that?",
    "My expertise is in project portfolio optimization. 📋 Let me know if I can help.",
    "Shall we return to portfolio optimization? 📊 I’m ready to assist!",
    "If you have portfolio-related questions, I’d be glad to help. 📈",
    "Why did the portfolio manager break up with their stock? It just wasn’t providing the right returns!",
    "My portfolio is like a bad romance: full of promises, but in the end, I’m left with nothing!",
    "I tried optimizing my portfolio for happiness… turns out it’s not correlated with my returns.",
    "Why did the bond break up with the stock? Too much volatility in the relationship!",
    "I asked my portfolio manager for advice. They said, 'Diversify your assets and your expectations!'",
    "Why don't portfolios ever get lonely? Because they’re always seeking new connections!",
    "My portfolio is like my diet: lots of planning, but the returns never quite match the effort.",
    "Why did the portfolio manager carry an umbrella? Because the forecast showed 100% chance of returns!",
    "What’s a portfolio’s favorite dance move? The re-balancing act!",
    "Why don’t stock traders read books on optimization? Too many variables to take into account!",
    "I told my portfolio manager to make it 'exciting.' Now it’s just a roller coaster of volatility!",
    "How do portfolio managers greet each other? ‘Keep it balanced!’",
    "My portfolio and I have one thing in common: we’re both good at losing interest!",
    "I tried optimizing my portfolio for gains, but it came back as 'zero risk, zero reward!'",
    "What’s a portfolio manager’s least favorite candy? Bear markets!",
    "Why did the portfolio optimizer go to therapy? Too many conflicting goals!",
    "Why are portfolios so reliable? They always give you a return… eventually!",
    "Diversifying is like dating: you spread the risk and hope one of them works out.",
    "Why did the mutual fund blush? Because it saw the portfolio rebalancing!",
    "My portfolio is like my mood swings: unpredictable and all over the place!"
]

STICKERS = {
    'yes': [
        'CAACAgIAAxkBAAENFc9nLSue_4HKBIVGuKnBHln-6tX1DAACQEAAAuCjggchglA_YPJLdTYE',
        'CAACAgIAAxkBAAENFcdnLStWszJ5OrQZXuPrlqvG9oQbdwAC0j8AAuCjggcQuD4Im2mRYTYE',
        'CAACAgIAAxkBAAENFcVnLStR4fyEsp9-9cftOOkOXAABz6sAAj9AAALgo4IHctyapLqff_s2BA',
        'CAACAgIAAxkBAAENFcNnLSs4JGzlT5YHnudJQE37nSSYcAAC1T8AAuCjggf7QUcah2mpxDYE'
    ],
    'hi':"CAACAgIAAxkBAAENFctnLSt1KUcDh2k60wRSjPy3G6PWogACT0AAAuCjggcuO1Eat5jdpzYE",
    'celebrate':["CAACAgIAAxkBAAENFc1nLSt-jDFTantylSPjaEWwy_nN8wAC6EoAAuCjggf4LTFlHEcvNDYE",
                 "CAACAgIAAxkBAAENFdFnLSwtibTgLKYAAaWigbxXoizGFWcAAsg_AALgo4IHmLnWjKAnNW82BA"
    ],
    'dont' : "CAACAgIAAxkBAAENFclnLStg8-ILs6G4c0Nm-rgQSthvrwACzD8AAuCjggfJsgrOQzbGKDYE",
    'error':[
        "CAACAgIAAxkBAAENFeBnLSyuEqHzFXEubRswsI4BW70hygACvj8AAuCjgge2wXu4Tter2DYE",
        "CAACAgIAAxkBAAENFd9nLSytZ-AQqTN2PY2jZWZfGWVCAwACvz8AAuCjggceXk69Po3C3jYE",
        "CAACAgIAAxkBAAENFd1nLSypmCg1uJ6Dg6ieoGbHyvU1zAACxj8AAuCjggc3_fw9DwABjtI2BA",
        "CAACAgIAAxkBAAENFdtnLSyno5Og3T38QI9DulG9C6hC0AAC0D8AAuCjggdIi703dNF3fzYE",
        "CAACAgIAAxkBAAENFdlnLSyjvNx5fD0CfmSKN6TvpInOEwAC0z8AAuCjggcSGbDgmNX7QDYE",
        "CAACAgIAAxkBAAENFddnLSyhvnwqvjo8WurkIQmV6lHspAAC2T8AAuCjggfGv4LPSS7JeDYE",
        "CAACAgIAAxkBAAENFdVnLSycnc4lCw0OBxOBZoXQA_VVCQACSkAAAuCjggfSHSqlNjsl6zYE",
        "CAACAgIAAxkBAAENFdNnLSySBTe-ja_KTjMaCv26MqXJWQAC30oAAuCjggesAAFLMtQsMDA2BA"
    ]
}