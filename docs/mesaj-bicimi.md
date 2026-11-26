# Çok Ajanlı Sistem — Ortak Mesaj Biçimi Belgesi

**Şirket:** EMİN SİGORTA (Grup D)  
**Ders:** VBA II  
**Yazar(lar):** Ayşe AYDIN (Çekirdek ve Arayüz) · Fatma Nisa ARSLAN (Junior Destek / Veri Sözlüğü)  
**Tarih:** 2026-11-26  
**Durum:** Taslak — İnceleme bekleniyor

---

## Amaç

Bu belge, EMİN SİGORTA'nın çok ajanlı sisteminde Çekirdek ve Arayüz bileşeninin ajanlar arasında taşıdığı mesajların **ortak yapısını ve alanlarını** tanımlar.  
Her ajan (Ajan 1, Ajan 2, Ajan 3), giriş ve çıkışlarını bu biçimde formatlar.  
Çekirdek bu biçimin doğruluğunu doğrular; uyumsuz mesajlar reddedilir.

---

## 1. Üst Veri (Envelope) — Her Mesajda Zorunlu

```json
{
  "envelope": {
    "msg_id": "string (UUID4)",
    "created_at": "string (ISO 8601, örn. '2026-11-26T10:00:00Z')",
    "source_agent": "string ('cekirdek' | 'ajan1' | 'ajan2' | 'ajan3')",
    "target_agent": "string ('cekirdek' | 'ajan1' | 'ajan2' | 'ajan3')",
    "run_id": "string (UUID4, tüm oturum boyunca sabit)",
    "seq": "integer (1'den başlar, her mesajda 1 artar)",
    "msg_type": "string (aşağıdaki türlerden biri)",
    "schema_version": "string (şu an '1.0')"
  }
}
```

### 1.1 Mesaj Türleri (`msg_type`)

| Tür | Açıklama |
|---|---|
| `task_request` | Çekirdek → Ajan: iş talebi |
| `task_result` | Ajan → Çekirdek: iş sonucu |
| `permission_request` | Ajan → Çekirdek: kullanıcı onayı isteniyor |
| `permission_response` | Çekirdek → Ajan: kullanıcı kararı iletiliyor |
| `progress_update` | Ajan → Çekirdek: ara durum bildirimi |
| `error` | Herhangi → Çekirdek: hata bildirimi |
| `retry_request` | Çekirdek → Ajan: işi geri al ve yeniden yap |

---

## 2. Yük (Payload) — `msg_type`'a Göre

### 2.1 `task_request`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "task_id": "string (UUID4)",
    "task_name": "string (örn. 'deprem-veri-topla')",
    "description": "string",
    "inputs": {
      "data_sources": ["string"],
      "parameters": {}
    },
    "deadline_sec": "integer (opsiyonel, saniye cinsinden zaman aşımı)"
  }
}
```

### 2.2 `task_result`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "task_id": "string (referans — hangi task_request'e yanıt)",
    "status": "string ('success' | 'partial' | 'failed')",
    "output": {
      "records": "integer (üretilen / işlenen kayıt sayısı)",
      "data_ref": "string (dosya yolu veya veri özeti)",
      "summary": "string (1-2 cümle açıklama)"
    },
    "tool_trace": [
      {
        "tool": "string (kullanılan araç adı, örn. 'playwright', 'pandas')",
        "command": "string",
        "started_at": "string (ISO 8601)",
        "finished_at": "string (ISO 8601)",
        "exit_code": "integer"
      }
    ],
    "source_ref": {
      "url": "string (veri çekilen kaynak URL, varsa)",
      "fetched_at": "string (ISO 8601)"
    }
  }
}
```

> **Not:** `tool_trace` dizisi boş bırakılamaz — Duyuru 10 kuralı gereği her araç kullanımının izi burada tutulur. İzsiz iş yapılmamış sayılır.

### 2.3 `permission_request`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "permission_id": "string (UUID4)",
    "task_id": "string",
    "action": "string (kullanıcıya gösterilecek eylem açıklaması)",
    "risk_level": "string ('low' | 'medium' | 'high')",
    "details": "string (opsiyonel ek bilgi)"
  }
}
```

### 2.4 `permission_response`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "permission_id": "string (referans)",
    "decision": "string ('approved' | 'rejected')",
    "decided_at": "string (ISO 8601)"
  }
}
```

### 2.5 `progress_update`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "task_id": "string",
    "step": "string (kısa açıklama, örn. 'AFAD sayfası yüklendi')",
    "percent": "integer (0–100, bilinmiyorsa -1)",
    "timestamp": "string (ISO 8601)"
  }
}
```

### 2.6 `error`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "task_id": "string",
    "error_code": "string",
    "error_message": "string",
    "recoverable": "boolean",
    "timestamp": "string (ISO 8601)"
  }
}
```

### 2.7 `retry_request`
```json
{
  "envelope": { "...": "..." },
  "payload": {
    "original_task_id": "string",
    "reason": "string",
    "adjustments": "object (opsiyonel, değişen parametreler)"
  }
}
```

---

## 3. Doğrulama Kuralları

| # | Kural | Uygulayan |
|---|---|---|
| V1 | `msg_id` UUID4 biçiminde olmalı | Çekirdek |
| V2 | `created_at` ve tüm tarih alanları ISO 8601 UTC biçiminde olmalı | Çekirdek |
| V3 | `source_agent` ve `target_agent` izin verilen değerlerden biri olmalı | Çekirdek |
| V4 | `seq` önceki değerden tam 1 fazla olmalı (sıra kontrolü) | Çekirdek |
| V5 | `task_result`'ta `tool_trace` dizisi en az 1 girdi içermeli | Çekirdek |
| V6 | `payload` alanı `msg_type`'a uygun zorunlu anahtarları içermeli | Çekirdek |
| V7 | `schema_version` bu belgenin versiyonuyla eşleşmeli | Çekirdek |

Doğrulama başarısız olursa Çekirdek `error` mesajı gönderir ve iş kaydedilmez.

---

## 4. Tam Örnek: Ajan 1 → Çekirdek Veri Teslimi

```json
{
  "envelope": {
    "msg_id": "b3d2a1f0-1234-4abc-8def-000000000001",
    "created_at": "2026-11-26T10:05:00Z",
    "source_agent": "ajan1",
    "target_agent": "cekirdek",
    "run_id": "a0b1c2d3-0000-4000-8000-000000000000",
    "seq": 3,
    "msg_type": "task_result",
    "schema_version": "1.0"
  },
  "payload": {
    "task_id": "task-ajan1-001",
    "status": "success",
    "output": {
      "records": 47,
      "data_ref": "data/deprem-son-24s.json",
      "summary": "AFAD portalından son 24 saatin 47 deprem kaydı toplandı; en büyük ML=4.1 (Kahramanmaraş, 2026-11-26T08:12:00Z)."
    },
    "tool_trace": [
      {
        "tool": "playwright",
        "command": "page.goto('https://deprem.afad.gov.tr/last-earthquakes.html')",
        "started_at": "2026-11-26T10:03:10Z",
        "finished_at": "2026-11-26T10:03:18Z",
        "exit_code": 0
      },
      {
        "tool": "playwright",
        "command": "page.locator('table#earthquakeTable').inner_html()",
        "started_at": "2026-11-26T10:03:18Z",
        "finished_at": "2026-11-26T10:03:19Z",
        "exit_code": 0
      }
    ],
    "source_ref": {
      "url": "https://deprem.afad.gov.tr/last-earthquakes.html",
      "fetched_at": "2026-11-26T10:03:20Z"
    }
  }
}
```

---

## 5. Veri Sözlüğü — Ortak Alanlar

> Bu bölüm Fatma Nisa ARSLAN (Junior Destek / Veri Sözlüğü) tarafından tamamlanacaktır.

| Alan Adı | Tip | Zorunlu | Açıklama | Örnek |
|---|---|---|---|---|
| `msg_id` | string (UUID4) | Evet | Mesajı benzersiz tanımlayan kimlik | `"b3d2a1f0-..."` |
| `created_at` | string (ISO 8601) | Evet | Mesajın oluşturulma zamanı (UTC) | `"2026-11-26T10:00:00Z"` |
| `source_agent` | enum | Evet | Gönderen ajan | `"ajan1"` |
| `target_agent` | enum | Evet | Alıcı ajan | `"cekirdek"` |
| `run_id` | string (UUID4) | Evet | Oturum kimliği (tüm mesajlarda aynı) | `"a0b1c2d3-..."` |
| `seq` | integer | Evet | Sıra numarası (1'den başlar) | `3` |
| `msg_type` | enum | Evet | Mesaj türü | `"task_result"` |
| `schema_version` | string | Evet | Şema versiyonu | `"1.0"` |
| `task_id` | string (UUID4) | Evet (payload) | İş birimi kimliği | `"task-ajan1-001"` |
| `tool_trace[].tool` | string | Evet | Kullanılan araç adı | `"playwright"` |
| `tool_trace[].command` | string | Evet | Çalıştırılan komut | `"page.goto(..."` |
| `tool_trace[].exit_code` | integer | Evet | Araç çıkış kodu (0=başarı) | `0` |
| `source_ref.url` | string | Hayır | Veri kaynağı URL'si | `"https://afad..."` |
| `source_ref.fetched_at` | string (ISO 8601) | Hayır | Veri çekilme zamanı | `"2026-11-26T10:03:20Z"` |

---

## 6. Değişiklik Geçmişi

| Versiyon | Tarih | Yazar | Değişiklik |
|---|---|---|---|
| 1.0 | 2026-11-26 | Ayşe AYDIN | İlk taslak oluşturuldu |
| — | — | Fatma Nisa ARSLAN | Bölüm 5 veri sözlüğü tamamlanacak |
