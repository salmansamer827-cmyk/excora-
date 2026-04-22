import { useEffect, useState } from "react";

export default function Watchlist() {
  const [list, setList] = useState<string[]>([]);

  useEffect(() => {
    fetch("https://excora.onrender.com/api/watchlist/user1")
      .then((res) => res.json())
      .then((data) => setList(data.watchlist));
  }, []);

  return (
    <div>
      <h3>Watchlist</h3>
      {list.map((item) => (
        <div key={item}>{item}</div>
      ))}
    </div>
  );
}