import { Search, ShoppingBag, SlidersHorizontal, Star } from 'lucide-react';
import { useMemo, useState } from 'react';
import DataTable from '../components/ui/DataTable.jsx';
import FloatingActionButton from '../components/ui/FloatingActionButton.jsx';
import GlassPanel from '../components/ui/GlassPanel.jsx';
import PageHeader from '../components/ui/PageHeader.jsx';
import { marketplaceItems } from '../data/mockData.js';

export default function Marketplace() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All');
  const categories = ['All', 'Seeds', 'Fertilizer', 'Equipment', 'Service'];
  const filteredItems = useMemo(
    () =>
      marketplaceItems.filter((item) => {
        const matchesQuery = `${item.title} ${item.seller} ${item.category}`.toLowerCase().includes(query.toLowerCase());
        const matchesCategory = category === 'All' || item.category === category;
        return matchesQuery && matchesCategory;
      }),
    [category, query]
  );

  return (
    <div className="space-y-6">
      <PageHeader eyebrow="Farmer commerce" title="Marketplace" description="Buy and sell inputs, equipment, produce, services, and precision agriculture packages." />
      <GlassPanel className="p-4">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
          <label className="relative min-w-0 flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="h-11 w-full rounded-lg border border-slate-200 bg-white/75 pl-10 pr-4 text-sm outline-none transition focus:border-agri-400 dark:border-white/10 dark:bg-white/8"
              placeholder="Search products, sellers, services..."
            />
          </label>
          <div className="flex flex-wrap gap-2">
            {categories.map((item) => (
              <button
                key={item}
                onClick={() => setCategory(item)}
                className={`inline-flex h-11 items-center gap-2 rounded-lg px-3 text-sm font-medium transition ${
                  category === item ? 'bg-agri-500 text-white shadow-glow' : 'border border-slate-200 bg-white/70 text-slate-700 dark:border-white/10 dark:bg-white/8 dark:text-slate-200'
                }`}
              >
                <SlidersHorizontal className="h-4 w-4" />
                {item}
              </button>
            ))}
          </div>
        </div>
      </GlassPanel>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {filteredItems.map((item) => (
          <GlassPanel key={item.title} className="p-5">
            <div className="flex items-start justify-between">
              <ShoppingBag className="h-6 w-6 text-agri-500" />
              <span className="inline-flex items-center gap-1 rounded-full bg-amber-300/16 px-2 py-1 text-xs font-semibold text-amber-600 dark:text-amber-300">
                <Star className="h-3.5 w-3.5 fill-current" />
                {item.rating}
              </span>
            </div>
            <p className="mt-4 text-lg font-semibold">{item.title}</p>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{item.category}</p>
            <div className="mt-5 flex items-end justify-between">
              <span className="text-2xl font-semibold">{item.price}</span>
              <span className="text-xs text-slate-500 dark:text-slate-400">{item.stock}</span>
            </div>
            <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">{item.seller} · {item.location} · {item.reviews} reviews</p>
          </GlassPanel>
        ))}
      </div>
      <GlassPanel className="p-5">
        <h2 className="mb-4 text-lg font-semibold">Listings</h2>
        <DataTable columns={[{ key: 'title', label: 'Item' }, { key: 'category', label: 'Category' }, { key: 'price', label: 'Price' }, { key: 'stock', label: 'Stock' }, { key: 'rating', label: 'Rating' }, { key: 'seller', label: 'Seller' }]} rows={filteredItems} />
      </GlassPanel>
      <FloatingActionButton />
    </div>
  );
}
