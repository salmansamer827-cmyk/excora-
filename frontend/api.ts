const BASE_URL = "https://excora.onrender.com/api";

export async function getPrice(symbol: string) {
  const res = await fetch(`${BASE_URL}/market/price/${symbol}`);
  return res.json();
}

export async function getWatchlist(user: string) {
  const res = await fetch(`${BASE_URL}/watchlist/${user}`);
  return res.json();
}