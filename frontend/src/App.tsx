import { useEffect, useState } from "react";
import { fetchQuote, fetchRecipes } from "./api";
import type { Quote, Recipe } from "./types";
import "./App.css";

function formatMoneyARS(n: number) {
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS" }).format(n);
}

function formatMoneyUSD(n: number) {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n);
}

function todayISO() {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, "0");
  const dd = String(d.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

export default function App() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loadingRecipes, setLoadingRecipes] = useState(true);

  const [recipeId, setRecipeId] = useState<number | "">("");
  const [date, setDate] = useState<string>(todayISO());

  const [quote, setQuote] = useState<Quote | null>(null);
  const [loadingQuote, setLoadingQuote] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // cargar recetas al iniciar
  useEffect(() => {
    (async () => {
      try {
        setLoadingRecipes(true);
        const data = await fetchRecipes();
        setRecipes(data);
      } catch (e: any) {
        setError(e?.message ?? "Error cargando recetas");
      } finally {
        setLoadingRecipes(false);
      }
    })();
  }, []);

  async function onQuote() {
    setError(null);
    setQuote(null);

    if (!recipeId) {
      setError("Por favor selecciona una receta");
      return;
    }
    if (!date) {
      setError("Por favor selecciona una fecha");
      return;
    }

    try {
      setLoadingQuote(true);
      const q = await fetchQuote(recipeId as number, date);
      setQuote(q);
    } catch (e: any) {
      setError(e?.message ?? "Error al obtener cotizacion");
    } finally {
      setLoadingQuote(false);
    }
  }

  return (
    <div className="container">
      <h1>WNS Challenge</h1>

      <div className="card">
        {loadingRecipes ? (
          <p>Cargando recetas…</p>
        ) : (
          <>
            <label>
              Recetas
              <select
                value={recipeId}
                onChange={(e) => setRecipeId(e.target.value ? Number(e.target.value) : "")}
              >
                <option value="">Selecciona una receta…</option>
                {recipes.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Selecciona una fecha
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </label>

            <button onClick={onQuote} disabled={loadingQuote}>
              {loadingQuote ? "Cotizando..." : "Obtener cotizacion"}
            </button>

          </>
        )}

        {error ? <p className="error">{error}</p> : null}
      </div>

      {quote ? (
        <div className="card">
          <h2>Resultados</h2>

          <div className="grid">
            <div>
              <div className="label">Receta</div>
              <div>{quote.recipe_name}</div>
            </div>
            <div>
              <div className="label">Fecha</div>
              <div>{quote.date}</div>
            </div>
            <div>
              <div className="label">USD→ARS</div>
              <div>{quote.usd_to_ars.toFixed(4)}</div>
            </div>
            <div>
              <div className="label">Total ARS</div>
              <div>{formatMoneyARS(quote.total_ars)}</div>
            </div>
            <div>
              <div className="label">Total USD</div>
              <div>{formatMoneyUSD(quote.total_usd)}</div>
            </div>
          </div>

          <h3>Ingredientes</h3>
          <div className="tableWrap">
            <table>
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Se necesita en gramos</th>
                  <th>Se va a comprar</th>
                  <th>Costo kg</th>
                  <th>Costo (ARS)</th>
                </tr>
              </thead>
              <tbody>
                {quote.items.map((it, idx) => (
                  <tr key={idx}>
                    <td>{it.name_raw}</td>
                    <td>{it.required_g}</td>
                    <td>{it.buy_g}</td>
                    <td>{it.cost_per_kg}</td>
                    <td>{formatMoneyARS(it.cost_ars)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {quote.instructions ? (
            <>
              <h3>Instrucciones para la preparacion</h3>
              <p style={{ whiteSpace: "pre-wrap" }}>{quote.instructions}</p>
            </>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}