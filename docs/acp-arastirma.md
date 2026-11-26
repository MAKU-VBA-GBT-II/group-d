# ACP Araştırma Notu — Haftalık Hazırlık

**Yazar:** Ayşe AYDIN (Çekirdek ve Arayüz)  
**Tarih:** 2026-11-26  
**Kaynak:** Duyuru 10 haftalık hazırlık maddelerinin araştırması

---

## ⚠️ Kritik Bulgu: İki Farklı "ACP" Var

Duyuruda geçen "ACP" teriminin tam olarak hangisini kastettiği netleştirilmeli:

| | IBM ACP | Zed ACP |
|---|---|---|
| **Tam adı** | Agent Communication Protocol | Agent Client Protocol |
| **Yapan** | IBM Research / BeeAI | Zed Industries |
| **Amacı** | Ajan ↔ Ajan arası iletişim | Editör/IDE ↔ Yapay zekâ ajanı |
| **Durum** | **Arşivlendi** (Ağustos 2025, A2A ile birleşti) | **Aktif** |
| **Altyapı** | REST / HTTP (JSON) | JSON-RPC 2.0 / stdio |
| **Site** | agentcommunicationprotocol.dev | agentclientprotocol.com |
| **GitHub** | github.com/i-am-bee/acp (arşiv) | github.com/agentclientprotocol/ |

> **Öneri:** PM aracılığıyla hocaya "projede hangi ACP kastediliyor?" diye sorulmalı.  
> Tahminim: Duyuru'daki `gemini --experimental-acp` örneği **Zed ACP** (stdio/JSON-RPC) olduğuna işaret ediyor.

---

## 1. Zed ACP (Aktif — Muhtemel Olan)

**Agent Client Protocol** — editörler ve kod ajanları arasındaki standart.  
Altyapı: JSON-RPC 2.0, `stdin/stdout` üzerinden.  

Resmi site: https://agentclientprotocol.com  
GitHub org: https://github.com/agentclientprotocol/

---

## 2. Claude Code'un ACP Desteği

Claude Code yerleşik ACP desteğiyle **gelmiyor**; bir adaptöre ihtiyaç var.

### Kullanılabilir Adaptörler

| Paket | Kaynak | Notlar |
|---|---|---|
| `@agentclientprotocol/claude-agent-acp` | npm (güncel) | Resmi Zed ACP adaptörü |
| `@zed-industries/claude-code-acp` | npm (eski, deprecated) | Aynı şeyin eski adı |

**Kurulum:**
```bash
npm install -g @agentclientprotocol/claude-agent-acp
```

**Çalıştırma:**
```bash
claude-agent-acp
# NOT: Kullanıcının kendi Claude Code aboneliğiyle çalışır — API anahtarı gerekmez
```

**Çalışma prensibi:**  
İstemci → JSON-RPC mesajı (`stdin`) → Adaptör → Claude Code (`claude --session-id ...`) → Yanıt (`stdout`) → İstemci

Desteklenen ACP metodları: `initialize`, `session/new`, `session/prompt`, `session/load`, `session/resume`, `fork`, `list`, `delete`.  
İzin istekleri ve araç çağrıları da adaptör üzerinden geçiyor.

### Minimum Test Betiği (Node.js)

```javascript
// test-acp.js
const { spawn } = require("child_process");
const readline = require("readline");

const proc = spawn("claude-agent-acp", [], { stdio: ["pipe", "pipe", "inherit"] });
const rl = readline.createInterface({ input: proc.stdout });

// 1. initialize
proc.stdin.write(JSON.stringify({
  jsonrpc: "2.0", id: 1, method: "initialize",
  params: { clientInfo: { name: "emin-sigorta-core", version: "0.1" } }
}) + "\n");

rl.on("line", (line) => {
  const msg = JSON.parse(line);
  if (msg.id === 1) {
    // 2. session aç ve "merhaba" gönder
    proc.stdin.write(JSON.stringify({
      jsonrpc: "2.0", id: 2, method: "session/new",
      params: { prompt: "Merhaba! Bağlantı testi. Tek cümleyle yanıtla." }
    }) + "\n");
  }
  if (msg.id === 2) {
    console.log("Claude Code yanıtı:", JSON.stringify(msg.result, null, 2));
    proc.kill();
  }
});
```

**Çalıştırma:**
```bash
node test-acp.js
```

> **Durum:** Betik test ortamında henüz çalıştırılmadı. Yeni duyuru gelmeden önce çalıştırıp sonuç Issue'ya eklenecek.

---

## 3. IBM ACP Python SDK (Yedek / Bilgi Amaçlı)

IBM ACP Ağustos 2025'te A2A ile birleştirildi; aktif geliştirme sona erdi.  
Ancak SDK hâlâ pip'ten kurulabiliyor ve çalışıyor.

```bash
pip install acp-sdk   # Python ≥ 3.11 gerekiyor
```

**Sunucu tarafı (örnek ajan):**
```python
import asyncio
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import Context, RunYield, RunYieldResume, Server

server = Server()

@server.agent()
async def merhaba(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Merhaba ACP ajanı"""
    yield Message(parts=[MessagePart(content="Merhaba EMİN SİGORTA!", content_type="text/plain")])

if __name__ == "__main__":
    server.run()   # http://localhost:8000
```

**İstemci tarafı:**
```python
import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

async def main():
    async with Client(base_url="http://localhost:8000") as client:
        run = await client.run_sync(
            agent="merhaba",
            input=[Message(parts=[MessagePart(content="Merhaba!", content_type="text/plain")])]
        )
        print("Yanıt:", run.output)

asyncio.run(main())
```

---

## 4. Gemini CLI'da ACP Desteği

```bash
# Kararlı bayrak (yeni sürümler)
gemini --acp

# Eski sürümlerde (hâlâ çalışıyor, deprecation uyarısı verebilir)
gemini --experimental-acp
```

**Çalışma prensibi:** Gemini CLI, `--acp` ile çalıştırıldığında `stdin/stdout` üzerinden JSON-RPC 2.0 mesajı dinleyen bir sunucuya dönüşüyor.

**Kimlik doğrulama notu:** `GEMINI_API_KEY` env değişkeni veya `gemini auth login` ile önceden giriş yapılmış olmalı; ACP modunda tarayıcı açılmıyor.  
Bu projenin kuralına uygun: **Kullanıcının kendi aboneliği** (kullanıcı `gemini auth login` yapmış olacak).

**Ekip açısından önemi:**  
Gemini kullanan 4 üye (Gülbahar, Emin, Ebru, Fatma Nisa) için Gemini CLI `--acp` desteği, hepsiyle aynı mesaj protokolüyle konuşmamızı sağlıyor.

| Araç | ACP Çalıştırma | Durum |
|---|---|---|
| Claude Code | `claude-agent-acp` adaptörü | Adaptör kurulumu gerekiyor |
| Gemini CLI | `gemini --acp` | Yerleşik destek var |
| Mistral Vibe | Araştırılıyor | — |

---

## 5. Açık Sorular (Hocaya / PM'e Sorulacak)

| # | Soru | Sorulacak Yer |
|---|---|---|
| S1 | Projede hangi ACP kasıt var — Zed ACP (stdio) mi, IBM ACP/A2A (HTTP) mi? | Hoca / Duyuru 11 |
| S2 | Gemini CLI `--acp` hocanın bilgisayarında kurulu/çalışıyor mu? | Hoca |
| S3 | Araç seçimi için ayar dosyası biçimi: `config.json` mi, `.env` mi? | Grup içi karar |

---

## 6. Sonraki Adımlar

- [ ] `@agentclientprotocol/claude-agent-acp` kur; test betiğini çalıştır, yanıtı kaydet.
- [ ] Gemini CLI `--acp` ile aynı betiği dene; çalışıyorsa not al.
- [ ] `docs/mesaj-bicimi.md` taslağını Fatma Nisa ile gözden geçir (Bölüm 5 veri sözlüğünü Fatma Nisa tamamlayacak).
- [ ] S1–S3 sorularını PM aracılığıyla hocaya ilet.
