import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "Enterprise IDP",
  description: "Internal Developer Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 ml-64 p-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
