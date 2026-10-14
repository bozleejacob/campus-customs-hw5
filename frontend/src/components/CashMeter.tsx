import { useEffect, useRef, useState } from "react";

interface Props {
  balance: number | null;
  asOf: string | null;
}

export function CashMeter({ balance, asOf }: Props) {
  const [flash, setFlash] = useState<"drop" | "same" | null>(null);
  const prev = useRef<number | null>(null);

  useEffect(() => {
    if (balance === null) return;
    const dropped = prev.current !== null && balance < prev.current;
    prev.current = balance;
    if (dropped) {
      setFlash("drop");
      const t = setTimeout(() => setFlash(null), 1200);
      return () => clearTimeout(t);
    }
  }, [balance]);

  const display =
    balance === null
      ? "—"
      : balance.toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
          maximumFractionDigits: 2,
        });

  return (
    <div className={`cash-meter ${flash === "drop" ? "cash-meter--drop" : ""}`}>
      <div className="cash-meter__label">Checking Balance</div>
      <div className="cash-meter__value">{display}</div>
      {asOf && <div className="cash-meter__asof">as of {asOf}</div>}
      {flash === "drop" && <div className="cash-meter__pulse">− paid out</div>}
    </div>
  );
}
