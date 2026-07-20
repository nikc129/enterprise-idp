"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Dashboard", icon: "📊" },
  { href: "/infrastructure", label: "Infrastructure", icon: "🏗️" },
  { href: "/infrastructure/ec2", label: "  Create EC2", icon: "🖥️" },
  { href: "/infrastructure/s3", label: "  Create S3", icon: "📦" },
  { href: "/infrastructure/vpc", label: "  Create VPC", icon: "🌐" },
  { href: "/infrastructure/rds", label: "  Create RDS", icon: "🗄️" },
  { href: "/deployment", label: "Deployments", icon: "🚀" },
  { href: "/monitoring", label: "Monitoring", icon: "📈" },
  { href: "/logs", label: "Logs", icon: "📝" },
  { href: "/ai", label: "AI Assistant", icon: "🤖" },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-gray-900 text-white p-4">
      <div className="mb-8">
        <h1 className="text-xl font-bold">Enterprise IDP</h1>
        <p className="text-xs text-gray-400 mt-1">Internal Developer Platform</p>
      </div>
      <nav>
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`block py-2 px-3 rounded mb-1 text-sm ${
              pathname === link.href
                ? "bg-blue-600 text-white"
                : "text-gray-300 hover:bg-gray-800"
            }`}
          >
            <span className="mr-2">{link.icon}</span>
            {link.label}
          </Link>
        ))}
      </nav>

    </aside>
  );
}
