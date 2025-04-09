import "./globals.css"
import { Inter } from "next/font/google"
import type React from "react" // Import React

const inter = Inter({ subsets: ["latin"] })

export const metadata = {
  title: "Grocheap -Grocery Search Engine",
  description: "Find and compare grocery prices in Montreal",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-green-50`}>{children}</body>
    </html>
  )
}



import './globals.css'