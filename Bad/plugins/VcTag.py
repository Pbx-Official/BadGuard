from Bad import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ " **❅ बेबी कहा हो। 🤗** ",
           " **❅ ओए सो गए क्या, ऑनलाइन आओ ।😊** ",
           " **❅ ओए वीसी आओ बात करते हैं । 😃** ",
           " **❅ खाना खाया कि नही। 🥲** ",
           " **❅ घर में सब कैसे हैं। 🥺** ",
           " **❅ पता है बहुत याद आ रही आपकी। 🤭** ",
           " **❅ और बताओ कैसे हो।..?? 🤨** ",
           " **❅ मेरी भी सैटिंग करवा दो प्लीज..?? 🙂** ",
           " **❅ आपका नाम क्या है।..?? 🥲** ",
           " **❅ नाश्ता हो गया..?? 😋** ",
           " **❅ मुझे अपने ग्रूप में ऐड कर लो। 😍** ",
           " **❅ आपका दोस्त आपको बुला रहा है। 😅** ",
           " **❅ मुझसे शादी करोगे ..?? 🤔** ",
           " **❅ सोने चले गए क्या 🙄** ",
           " **❅ अरे यार कोई AC चला दो 😕** ",
           " **❅ आप कहा से हो..?? 🙃** ",
           " **❅ हेलो जी नमस्ते 😛** ",
           " **❅ BABY क्या कर रही हो..? 🤔** ",
           " **❅ क्या आप मुझे जानते हो .? ☺️** ",
           " **❅ आओ baby Ludo खेलते है .🤗** ",
           " **❅ चलती है क्या 9 से 12... 😇** ",
           " **❅ आपके पापा क्या करते है 🤭** ",
           " **❅ आओ baby बाजार चलते है गोलगप्पे खाने। 🥺** ",
           " **❅ अकेली ना बाजार जाया करो, नज़र लग जायेगी। 😶** ",
           " **❅ और बताओ BF कैसा है ..?? 🤔** ",
           " **❅ गुड मॉर्निंग 😜** ",
           " **❅ मेरा एक काम करोगे। 🙂** ",
           " **❅ DJ वाले बाबू मेरा गाना चला दो। 😪** ",
           " **❅ आप से मिलकर अच्छा लगा।☺** ",
           " **❅ मेरे बाबू ने थाना थाया।..? 🙊** ",
           " **❅ पढ़ाई कैसी चल रही हैं ? 😺** ",
           " **❅ हम को प्यार हुआ। 🥲** ",
           " **❅ Nykaa कौन है...? 😅** ",
           " **❅ तू खींच मेरी फ़ोटो ..? 😅** ",
           " **❅ Phone काट मम्मी आ गई क्या। 😆** ",
           " **❅ और भाबी से कब मिल वा रहे हो । 😉** ",
           " **❅ क्या आप मुझसे प्यार करते हो 💚** ",
           " **❅ मैं तुम से बहुत प्यार करती हूं..? 👀** ",
           " **❅ बेबी एक kiss दो ना..?? 🙉** ",
           " **❅ एक जॉक सुनाऊं..? 😹** ",
           " **❅ vc पर आओ कुछ दिखाती हूं  😻** ",
           " **❅ क्या तुम instagram चलते हो..?? 🙃** ",
           " **❅ whatsapp नंबर दो ना अपना..? 😕** ",
           " **❅ आप की दोस्त से मेरी सेटिंग करा दो ..? 🙃** ",
           " **❅ सारा काम हो गया हो तो ऑनलाइन आ जाओ।..? 🙃** ",
           " **❅ कहा से हो आप 😊** ",
           " **❅ जा तुझे आज़ाद कर दिया मैंने मेरे दिल से। 🥺** ",
           " **❅ मेरा एक काम करोगे, ग्रूप मे कुछ मेंबर ऐड कर दो ..? ♥️** ",
           " **❅ मैं तुमसे नाराज़ हूं 😠** ",
           " **❅ आपकी फैमिली कैसी है..? ❤** ",
           " **❅ क्या हुआ..? 🤔** ",
           " **❅ बहुत याद आ रही है आपकी 😒** ",
           " **❅ भूल गए मुझे 😏** ",
           " **❅ झूठ क्यों बोला आपने मुझसे 🤐** ",
           " **❅ इतना भाव मत खाया करो, रोटी खाया करो कम से कम मोटी तो हो जाओगी 😒** ",
           " **❅ ये attitude किसे दिखा रहे हो 😮** ",
           " **❅ हेमलो कहा busy ho 👀** ",
           " **❅ आपके जैसा दोस्त पाकर मे बहुत खुश हूं। 🙈** ",
           " **❅ आज मन बहुत उदास है ☹️** ",
           " **❅ मुझसे भी बात कर लो ना 🥺** ",
           " **❅ आज खाने में क्या बनाया है 👀** ",
           " **❅ क्या चल रहा है 🙂** ",
           " **❅ message क्यों नहीं करती हो..🥺** ",
           " **❅ मैं मासूम हूं ना 🥺** ",
           " **❅ कल मज़ा आया था ना 😅** ",
           " **❅ कल कहा busy थे 😕** ",
           " **❅ आप relationship में हो क्या..? 👀** ",
           " **❅ कितने शांत रहते हो यार आप 😼** ",
           " **❅ आपको गाना, गाना आता है..? 😸** ",
           " **❅ घूमने चलोगे मेरे साथ..?? 🙈** ",
           " **❅ हमेशा हैप्पी रहा करो यार 🤞** ",
           " **❅ क्या हम दोस्त बन सकते है...? 🥰** ",
           " **❅ आप का विवाह हो गया क्या.. 🥺** ",
           " **❅ कहा busy the इतने दिनों से 🥲** ",
           " **❅ single हो या mingle 😉** ",
           " **❅ आओ पार्टी करते है 🥳** ",
           " **❅ Bio में link हैं join कर लो 🧐** ",
           " **❅ मैं तुमसे प्यार नहीं करती, 🥺** ",
           " **❅ यहां आ जाओ ना @IND_PAWAN मस्ती करेंगे 🤭** ",
           " **❅ भूल जाओ मुझे,..? 😊** ",
           " **❅ अपना बना ले पिया, अपना बना ले 🥺** ",
           " **❅ मेरा ग्रुप भी join कर लो ना 🤗** ",
           " **❅ मैने तेरा नाम Dil rakh diya 😗** ",
           " **❅ तुमारे सारे दोस्त कहा गए 🥺** ",
           " **❅ my cute owner @PAWAN_IS_BACK 🥰** ",
           " **❅ किसकी याद मे खोए हो जान 😜** ",
           " **❅ गुड नाईट जी बहुत रात हो गई 🥰** ",
           ]

VC_TAG = [ " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ 2024, ᴅᴇᴀʀ🍷...**",
         " **๛ ᴍᴀʏ ᴛʜɪs ʏᴇᴀʀ ʙʀɪɴɢ ʏᴏᴜ ᴊᴏʏ, ʜᴀᴘᴘɪɴᴇss, ᴀɴᴅ ɢᴏᴏᴅ ʜᴇᴀʟᴛʜ. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🥂...**",
         " **๛ ᴡɪsʜɪɴɢ ʏᴏᴜ sᴜᴄᴄᴇss ɪɴ ᴀᴄʜɪᴇᴠɪɴɢ ᴀʟʟ ʏᴏᴜʀ ɢᴏᴀʟs ᴀɴᴅ ᴅʀᴇᴀᴍs ɪɴ ᴛʜᴇ ᴄᴏᴍɪɴɢ ʏᴇᴀʀ.🥂...**",
         " **๛ ᴍᴀʏ ᴛʜᴇ ᴜᴘᴄᴏᴍɪɴɢ ʏᴇᴀʀ ʙᴇ ғɪʟʟᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ, ʟᴀᴜɢʜᴛᴇʀ, ᴀɴᴅ ɴᴇᴡ ᴏᴘᴘᴏʀᴛᴜɴɪᴛɪᴇs.🍷...**",
         " **๛ ʜᴇʀᴇ's ᴛᴏ ᴀɴᴏᴛʜᴇʀ ʏᴇᴀʀ ᴏғ ʙʟᴇssɪɴɢs ᴀɴᴅ ɴᴇᴡ ʙᴇɢɪɴɴɪɴɢs. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🍷...**",
         " **๛ ᴍᴀʏ ʏᴏᴜʀ ᴅᴀʏs ʙᴇ ғɪʟʟᴇᴅ ᴡɪᴛʜ sᴜɴsʜɪɴᴇ ᴀɴᴅ ʏᴏᴜʀ ɴɪɢʜᴛs ʙᴇ ғɪʟʟᴇᴅ ᴡɪᴛʜ ʟᴏᴠᴇ. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🥂...**",
         " **๛ ᴡɪsʜɪɴɢ ʏᴏᴜ sᴛʀᴇɴɢᴛʜ ᴀɴᴅ ᴘᴇʀsᴇᴠᴇʀᴀɴᴄᴇ ᴛᴏ ᴏᴠᴇʀᴄᴏᴍᴇ ᴀɴʏ ᴄʜᴀʟʟᴇɴɢᴇs ᴛʜᴀᴛ ᴄᴏᴍᴇ ʏᴏᴜʀ ᴡᴀʏ. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🍻...**",
         " **๛ ᴍᴀʏ ᴛʜɪs ʏᴇᴀʀ ʙᴇ ᴀ ʏᴇᴀʀ ᴏғ ɢʀᴏᴡᴛʜ, ʜᴀᴘᴘɪɴᴇss, ᴀɴᴅ sᴜᴄᴄᴇss ғᴏʀ ʏᴏᴜ. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🍺...**",
         " **๛ ᴡɪsʜɪɴɢ ʏᴏᴜ ᴀ ʏᴇᴀʀ ғɪʟʟᴇᴅ ᴡɪᴛʜ ᴇxᴄɪᴛᴇᴍᴇɴᴛ, ᴀᴅᴠᴇɴᴛᴜʀᴇ, ᴀɴᴅ ᴜɴғᴏʀɢᴇᴛᴛᴀʙʟᴇ ᴍᴏᴍᴇɴᴛs. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🍾...**",
         " **๛ ᴍᴀʏ ᴛʜɪs ʏᴇᴀʀ ʙʀɪɴɢ ʏᴏᴜ ᴄʟᴏsᴇʀ ᴛᴏ ʏᴏᴜʀ ʟᴏᴠᴇᴅ ᴏɴᴇs ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ʙᴇᴀᴜᴛɪғᴜʟ ᴍᴇᴍᴏʀɪᴇs. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🧉...**",
         " **๛ ᴄʜᴇᴇʀs ᴛᴏ ᴀ ʙʀᴀɴᴅ ɴᴇᴡ ᴄʜᴀᴘᴛᴇʀ ᴏғ ʏᴏᴜʀ ʟɪғᴇ. ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ!🍹...**",
         " **๛ ᴄʜᴇᴇʀs ᴛᴏ 2024 ᴀs ᴀ ɴᴇᴡ ʏᴇᴀʀ!🍷...**",
         " **๛ ɪ'ᴍ ᴡɪsʜɪɴɢ ʏᴏᴜ ᴀ ɢᴏᴏᴅ ɴᴇᴡ ʏᴇᴀʀ & ᴀ ᴘʀᴏsᴘᴇʀᴏᴜs ʟɪғᴇ🧋...**",
         " **๛ ᴍᴀʏ ᴛʜɪs ʏᴇᴀʀ ʙᴇ ғɪʟʟᴇᴅ ᴡɪᴛʜ ᴘʀᴏsᴘᴇʀɪᴛʏ ғᴏʀ ʏᴏᴜ!🧃...**",
         " **๛ ɪ ʜᴏᴘᴇ ʏᴏᴜ ʜᴀᴠᴇ 365 ᴅᴀʏs ᴏғ ᴜɴᴇɴᴅɪɴɢ ᴊᴏʏ ɪɴ 2024☕...**",
         " **๛ ʟᴇᴛ ᴛʜᴇ ᴄᴏᴍɪɴɢ sᴇᴀsᴏɴ ʙᴇɢɪɴ ᴡɪᴛʜ ᴀsᴛᴏɴɪsʜᴍᴇɴᴛ ᴀɴᴅ ʜᴀᴘᴘɪɴᴇss, ᴍʏ ʟᴏᴠᴇ🥛...**",
         " **๛ ɪ ʜᴏᴘᴇ ᴛʜɪs ʏᴇᴀʀ ᴛᴜʀɴs ᴏᴜᴛ ᴛᴏ ʙᴇ ᴛʜᴇ ʙᴇsᴛ ʏᴇᴀʀ ᴏғ ʏᴏᴜʀ ʟɪғᴇ ᴀɴᴅ ʏᴏᴜʀ ғᴀᴍɪʟʏ ᴛᴏᴏ🍷...**",
         " **๛ ɪ ᴡɪsʜ ʏᴏᴜ ᴀʟʟ ᴛʜᴇ ʙʟᴇssɪɴɢs ᴀɴᴅ sᴜᴄᴄᴇss ʏᴏᴜ ᴛʀᴜʟʏ ᴅᴇsᴇʀᴠᴇ🍸...**",
         " **๛ ɪ ᴘʀᴏᴍɪsᴇ ᴛᴏ ʙᴇ ᴡɪᴛʜ ʏᴏᴜ ᴇᴠᴇʀʏ sɪɴɢʟᴇ ᴅᴀʏ ɪɴ ᴛʜᴇ ᴄᴏᴍɪɴɢ ʏᴇᴀʀ🍸...**",
         " **๛ ʏᴏᴜ ʟɪᴠᴇᴅ ᴛʜᴇ ɢᴏᴏᴅ ʟɪғᴇ ʟᴀsᴛ ʏᴇᴀʀ, ʙᴜᴛ ᴛʜɪs ʏᴇᴀʀ ɪ ʜᴏᴘᴇ ʏᴏᴜ ʟɪᴠᴇ ʏᴏᴜʀ ʙᴇsᴛ ʟɪғᴇ!🧉...**",
         " **๛ ᴍᴀʏ ʏᴏᴜʀ ʜᴇᴀʀᴛ ʙᴇ ʟɪɢʜᴛ, ʏᴏᴜʀ ᴅᴀʏs ʙᴇ ʙʀɪɢʜᴛ, ᴀɴᴅ ʏᴏᴜʀ ʏᴇᴀʀ ʙᴇ ᴊᴜsᴛ ʀɪɢʜᴛ!🍾...**",
         " **๛ ɪɴ 2024, ᴍᴀʏ ʏᴏᴜʀ ɢʟᴀss ʙᴇ ʜᴀʟғ ғᴜʟʟ — ᴏғ ᴄʜᴀᴍᴘᴀɢɴᴇ ᴛʜᴀᴛ ɪs!🥤...**",
         " **๛ ɴᴇᴡ ʙᴇɢɪɴɴɪɴɢs ᴀʀᴇ ᴊᴜsᴛ ᴀʀᴏᴜɴᴅ ᴛʜᴇ ᴄᴏʀɴᴇʀ🎉...**",
         " **๛ ᴇᴋ ᴛᴏ ᴀᴀᴘ ᴍᴜsᴋᴜʀᴀᴀᴛᴇ ʙᴀʜᴜᴛ ʜᴏ, ᴀᴜʀ ᴘʜɪʀ sʜᴀʀᴍᴀᴀᴛᴇ ʙᴀʜᴜᴛ ʜᴏ, ᴅɪʟ ᴛᴏ ᴄʜᴀᴀʜᴀᴛᴀ ʜᴀɪ ᴀᴀᴘᴀᴋᴏ ɴᴇᴡ ʏᴇᴀʀ ᴘᴀʀᴛʏ ᴍᴇɪɴ ʙᴜʟᴀᴏᴏɴ , ᴘᴀʀ sᴜɴᴀ ʜᴀɪ ᴀᴀᴘ ᴋʜᴀᴀᴛᴇ ʙᴀʜᴜᴛ ʜᴏ. 🍷🎁...**",
         " **๛ ᴇᴋ ʜᴀᴀᴛʜ ᴍᴇɪɴ ᴄʜɪᴋᴀɴ ᴅᴏᴏsᴀʀᴇ ʜᴀᴀᴛʜ ᴍᴇɪɴ ʜᴀɪ ʙɪʏᴀʀ, ᴊᴀᴍᴀᴋᴀʀ ᴘɪʏᴏ ᴍᴇʀᴇ ʏᴀᴀʀᴏ, ᴋʏᴏɴᴋɪ ᴀᴀ ɢᴀʏᴀ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ🍷🎁...**",
         " **๛ ᴄᴏᴡ ᴅᴏᴏᴅʜ ᴅᴇᴛɪ ʜᴀɪ ʟᴀᴀᴛ ᴍᴀᴀʀᴀᴋᴀʀ, ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ᴀᴀɴᴋʜ ᴍᴀᴀʀ ᴋᴀʀ.🎉🎁...**",
         " **๛ ᴀᴀʟᴏᴏ sᴀᴅᴇ-sᴀᴅᴇ...ᴛᴀᴍᴀᴀᴛᴀʀ sᴀᴅᴇ-sᴀᴅᴇ... ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ᴀᴀᴘᴀᴋᴏ ʀᴀᴊᴀᴀɪ ᴍᴇɪɴ ᴘᴀᴅᴇ-ᴘᴀᴅᴇ. 🍷🎁...**",
         " **๛ ᴄʜᴏᴏʜᴀ ɴɪᴋᴀʟᴀ ʙɪʟ sᴇ, ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ᴅɪʟ sᴇ !🎉...**",
         " **๛ ᴘᴜʀᴀᴀɴᴀ ᴘʏᴀᴀʀ ᴋʜᴀᴛᴍ ʜᴏ ɢᴀʏᴀ, ɴʏᴀ ᴘʏᴀᴀʀ ᴋɪ ᴛᴀʟᴀᴀsʜ ʜᴀɪ ᴊᴀᴀʀɪ, 1 ᴊᴀɴᴜᴀʀʏ ᴋᴏ ᴍᴏʜᴀʙʙᴀᴛ ᴋᴀ ɪᴊᴀʜᴀᴀʀ ᴋᴀʜɪ ᴘᴀᴅ ɴᴀ ᴊᴀᴇ ᴀᴀᴘᴀᴋᴏ ʙʜᴀᴀʀᴇᴇ,  ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ 💥...**",
         " **๛ ᴛᴜᴍ ʜᴏ ᴘʀᴀᴀɴᴏɴ sᴇ ᴘʏᴀᴀʀᴇ, ᴘʀᴀᴀɴ ʜᴀᴍᴀᴀʀᴇ, ᴊɪɴᴅᴀɢᴇᴇ ᴍᴇɪɴ ʙᴀɴᴀᴋᴀʀ ᴀᴀᴇ ᴍᴇʜᴀᴍᴀᴀɴ ʜᴀᴍᴀᴀʀᴇ, ᴅʜᴇᴇʀᴇ ᴅʜᴇᴇʀᴇ ᴊɪɴᴅᴀɢᴇᴇ ʜᴏ ɢᴀᴇᴇ ɢᴜʟᴀᴀᴍ ᴛᴜᴍʜᴀᴀʀᴇᴇ ʟᴇ ʟᴏ ɴᴀʏ sᴀᴀʟ ᴋᴇᴇ sʜᴜʙʜᴀᴋᴀᴀᴍᴀɴᴀᴇɴ ʜᴀᴍᴀᴀʀᴇᴇ !✨...**", 
         " **๛ ɴᴀʏᴀ ᴊᴀᴍᴀᴀɴᴀ ʜᴀɪ ɴᴀʏᴀ ᴛʜɪᴋᴀᴀɴᴀ ʜᴀɪ, ᴄʜᴀʟ ᴘᴀᴅᴇ ʜᴀɪ ᴀɪsᴇᴇ ʀᴀᴀʜ ᴘᴀʀ ᴀʙ ᴅᴏᴏʀ ᴛʜɪᴋᴀᴀɴᴀ ʜᴀɪ, ᴊᴀᴀɴᴀ ʜᴀɪ ᴜsᴇ ᴍᴀɴᴊɪʟ ᴘᴀʀ , ᴊᴀʜᴀᴀɴ ɴᴀʏᴀ sᴀᴀʟ ᴍᴀᴀɴᴀɴᴀ ʜᴀɪ 💥...**",
         " **๛ sʜᴜʙʜᴀᴍᴀʏ 😁 ᴍᴀɴɢᴀʟᴀᴍᴀʏ ʟᴀᴀʙʜᴀᴍᴀʏ ʜᴏ ᴀɪsᴇᴇ ᴋᴀᴀᴍᴀɴᴀ!! sᴠᴀsᴛʜ ʀᴀʜᴏ 😍 ᴍᴀsᴛ ʀᴀʜᴏ sᴀᴅᴀ 😍 ʜᴀɴsᴀᴛᴇ ʀᴀʜᴏ ʜᴀɴsᴀᴀᴛᴇ ʀᴀʜᴏ!!! ʜᴀᴘᴘʏ 😍 ɴᴇᴡ ʏᴇᴀʀ ᴅᴏsᴛᴏɴ! !!!✨🎁...**",
         " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ 2024 🍷🎁...**",
         " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ʙᴀʙʏᴅᴏʟʟ 🍷😻...**",
         " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ᴊᴀᴀɴᴇᴍᴀɴ 💫...**",
         " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ᴅᴏsᴛ 💫🎁...**",
         " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ ʙᴀʙʏ 🍷🎁...**",
         " **๛ ʜᴀᴘᴘʏ ɴᴇᴡ ʏᴇᴀʀ 🎁...**",
        ]


@app.on_message(filters.command(["hitag" ], prefixes=["/", "@", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")

    if message.reply_to_message and message.text:
        return await message.reply("/hitag ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/hitag ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("/hitag ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["ntag"], prefixes=["/", "@", "#"]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("๏ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs. ")
    if chat_id in spam_chats:
        return await message.reply("๏ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@app.on_message(filters.command(["cancel", "histop", "nstop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("๏ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("๏ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("๏ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ๏")
