import './globals.css';

export const metadata = {
  title: 'AI Road Crash Analytics Dashboard | ปวช. 2568 - 2572',
  description: 'ระบบวิเคราะห์ข้อมูลและโทรมาตรอุบัติเหตุทางถนน 194,726 รายการ การแข่งขันทักษะวิชาชีพ สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์ ระดับ ปวช.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="th">
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-800 antialiased">
        {children}
      </body>
    </html>
  );
}
