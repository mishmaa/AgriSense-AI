export function cn(...classes) {
  return classes.filter(Boolean).join(' ');
}

export function formatPercent(value) {
  return `${Math.round(Number(value))}%`;
}

export function formatNumber(value, digits = 0) {
  return new Intl.NumberFormat('en', {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits
  }).format(Number(value));
}
