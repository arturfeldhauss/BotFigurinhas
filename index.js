const { default: makeWASocket, useMultiFileAuthState, downloadMediaMessage } = require("@whiskeysockets/baileys")
const qrcode = require("qrcode-terminal")
const sharp = require("sharp")

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState("auth")

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false,
    })

    sock.ev.on("connection.update", (update) => {
        const { connection, qr } = update
        if (qr) {
            qrcode.generate(qr, { small: true })
        }

        if (connection === "open") {
            console.log("✅ Conectado ao WhatsApp com sucesso!")
        } else if (connection === "close") {
            console.log("❌ Conexão encerrada. Tentando reconectar...")
            startBot()
        }
    })

    sock.ev.on("creds.update", saveCreds)

    sock.ev.on("messages.upsert", async ({ messages }) => {
        const msg = messages[0]
        if (!msg.message || msg.key.fromMe) return

        const from = msg.key.remoteJid
        const isImage = msg.message.imageMessage

        if (isImage) {
            try {
                // Baixa a imagem
                const buffer = await downloadMediaMessage(msg, "buffer", {}, { logger: console })

                // Converte para figurinha
                const stickerBuffer = await sharp(buffer)
                    .resize(512, 512, { fit: "contain" })
                    .webp()
                    .toBuffer()

                // Envia a figurinha de volta
                await sock.sendMessage(from, {
                    sticker: stickerBuffer,
                })

                console.log("🖼️ Figurinha enviada com sucesso!")
            } catch (error) {
                console.error("Erro ao processar imagem:", error)
                await sock.sendMessage(from, { text: "❌ Erro ao criar a figurinha." })
            }
        } else {
            const text = msg.message?.conversation || msg.message?.extendedTextMessage?.text
            if (text?.toLowerCase().includes("figurinha")) {
                await sock.sendMessage(from, {
                    text: "📸 Me envie uma imagem que eu transformo em figurinha!",
                })
            }
        }
    })
}

startBot()
