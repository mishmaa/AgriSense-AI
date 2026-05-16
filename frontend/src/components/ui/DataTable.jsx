export default function DataTable({ columns, rows }) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200/70 dark:border-white/10">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200/70 text-sm dark:divide-white/10">
          <thead className="bg-slate-50/80 dark:bg-white/5">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="whitespace-nowrap px-4 py-3 text-left font-medium text-slate-500 dark:text-slate-400">
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200/70 dark:divide-white/10">
            {rows.map((row, index) => (
              <tr key={`${row[columns[0].key]}-${index}`} className="bg-white/35 transition hover:bg-agri-500/8 dark:bg-white/[0.02]">
                {columns.map((column) => (
                  <td key={column.key} className="whitespace-nowrap px-4 py-3 text-slate-700 dark:text-slate-200">
                    {row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
