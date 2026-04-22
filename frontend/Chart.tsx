import { useEffect, useState } from "react";

export default function Chart({ symbol }: { symbol: string }) {
  const [price, setPrice] = useState(0);

  useEffect(() => {
    const fetchPrice = async () => {
      const res = await fetch(
        `https://excora.onrender.com/api/market/price/${symbol}`
      );
      const data = await res.json();
      setPrice(data.price);
    };

    fetchPrice();
    const interval = setInterval(fetchPrice, 3000);

    return () => clearInterval(interval);
  }, [symbol]);

  return (
    <div>
      <h2>{symbol}</h2>
      <h1>${price}</h1>

      {/* لاحقاً نضيف TradingView chart هنا */}
    </div>
  );
}