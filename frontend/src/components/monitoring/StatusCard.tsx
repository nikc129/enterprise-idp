interface StatusCardProps {
  title: string;
  value: number | string;
  icon: string;
  color: string;
  subtitle?: string;
}

const colorMap: Record<string, string> = {
  blue: "bg-blue-50 border-blue-200",
  green: "bg-green-50 border-green-200",
  purple: "bg-purple-50 border-purple-200",
  orange: "bg-orange-50 border-orange-200",
  red: "bg-red-50 border-red-200",
};

export default function StatusCard({ title, value, icon, color, subtitle }: StatusCardProps) {
  return (
    <div className={`rounded-lg border-2 p-6 ${colorMap[color] || colorMap.blue}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-3xl font-bold mt-1">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
    </div>
  );
}
