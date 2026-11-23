# คู่มือขั้นตอนการนำระบบขึ้นสู่คลาวด์ออนไลน์ (Dual-Cloud Deployment Guide)
## AI Road Crash Analytics Dashboard | การแข่งขันทักษะวิชาชีพ ปวช. 2568
### สถาปัตยกรรมผสมผสาน: Streamlit Community Cloud + Vercel Web Portal

---

## 🌟 ทำไมต้องใช้สถาปัตยกรรมคู่ (Dual-Cloud Hybrid Architecture)?

ตามเกณฑ์การตัดสินข้อ **3.5.5 (ความพร้อมใช้งานจริง 3 คะแนน)** และ **3.5.6 (ประสิทธิภาพ Performance 5 คะแนน)**:
* **Streamlit Community Cloud** (ฟรี 100%): ทำหน้าที่เป็น **Analytics Engine** ประมวลผล Python และ WebSockets แบบ Persistent โหลดข้อมูล 194,726 แถวเข้า RAM ตอบสนองการคลิกฟิลเตอร์ได้ใน $<200$ ms อย่างมีเสถียรภาพสูงสุด
* **Vercel** (ฟรี 100%): ทำหน้าที่เป็น **Executive Web Portal** บนโดเมน `*.vercel.app` เพื่อแสดงภาพรวมโครงการ เมตริกสรุป และหน้ากากครอบแดชบอร์ดระดับพรีเมียม

---

## 🚀 ขั้นตอนที่ 1: Deploy บน Streamlit Community Cloud (ใช้เวลา 1 นาที)

1. เข้าเว็บไซต์ [https://share.streamlit.io](https://share.streamlit.io)
2. คลิกปุ่ม **"Continue with GitHub"** และเข้าสู่ระบบด้วยบัญชี GitHub ของคุณ
3. คลิกปุ่มสีฟ้า **"New app"** (มุมขวาบน)
4. กรอกข้อมูลการเชื่อมต่อ:
   * **Repository**: เลือก `APWINE-70/AI_Crash_Dashboard`
   * **Branch**: `main`
   * **Main file path**: `app.py`
   * **App URL** (เลือกได้ตามต้องการ): เช่น `ai-crash-dashboard` (จะได้ `https://ai-crash-dashboard.streamlit.app`)
5. คลิกปุ่ม **"Deploy!"**
6. รอระบบ Build ประมาณ 1–2 นาที หน้าแดชบอร์ดจะเปิดใช้งานแบบสาธารณะทันที!
7. **คัดลอก URL ของคุณไว้** (เช่น `https://ai-crash-dashboard.streamlit.app`)

---

## ⚡ ขั้นตอนที่ 2: Deploy Web Portal บน Vercel (ใช้เวลา 1 นาที)

1. เข้าเว็บไซต์ [https://vercel.com](https://vercel.com)
2. เข้าสู่ระบบด้วยบัญชี **GitHub**
3. ที่หน้าแดชบอร์ด คลิกปุ่ม **"Add New..."** $\rightarrow$ เลือก **"Project"**
4. ในส่วน **"Import Git Repository"** ค้นหาและคลิกปุ่ม **"Import"** ที่ Repository `APWINE-70/AI_Crash_Dashboard`
5. ในหน้าตั้งค่าโปรเจกต์:
   * **Project Name**: `ai-crash-dashboard` (หรือตามต้องการ)
   * **Framework Preset**: เลือก **"Other"** (ระบบจะตรวจจับ `index.html` และ `vercel.json` อัตโนมัติ)
   * **Root Directory**: `./` (ค่าเริ่มต้น)
6. คลิกปุ่ม **"Deploy"**
7. รอประมาณ 20 วินาที Vercel จะแสดงผลสำเร็จพร้อมมอบลิงก์ เช่น `https://ai-crash-dashboard-wine.vercel.app`!
8. เปิดลิงก์ Vercel ของคุณ $\rightarrow$ นำ URL ที่ได้จาก Streamlit Cloud ในขั้นตอนที่ 1 มาวางลงในช่อง **"กำหนด URL ของ Streamlit Cloud"** แล้วกด **"อัปเดต URL"**
9. ระบบ Vercel จะจดจำและเชื่อมต่อเข้ากับแดชบอร์ดอัตโนมัติแบบไร้รอยต่อ!

---

## 💻 แผนสำรอง: การใช้งานแบบ Offline บนเครื่อง (Local Fallback)

ตามข้อกำหนดของเกณฑ์ 3.5.5 หากระบบออนไลน์ติดขัด ให้มีแผนสำรองที่รันบนเครื่องได้สมบูรณ์:
1. เปิด Terminal / PowerShell ที่โฟลเดอร์โปรเจกต์:
   ```powershell
   cd C:\adisak\AI
   ```
2. สั่งรันคำสั่ง:
   ```powershell
   streamlit run app.py
   ```
3. แดชบอร์ดจะเปิดขึ้นที่ `http://localhost:8501` พร้อมข้อมูล 194,726 แถวทันที
