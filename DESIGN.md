\# DESIGN.md



\## Tema \& Colori



\### Background

\- \*\*Body principale:\*\* `#111827` (gray-900) — scuro profondo

\- \*\*Sidebar:\*\* Gradiente lineare `#1f2937 → #131928` (gray-800 → quasi nero con lieve sfumatura indaco)

\- \*\*Card/media:\*\* `#1f2937` (gray-800)

\- \*\*Input/select:\*\* `#374151` (gray-700)

\- \*\*Overlay modali:\*\* `rgba(17, 24, 39, 0.8)` (gray-900 semi-trasparente)

\- \*\*Tooltip/dropdown:\*\* `#1f2937` (gray-800)



\### Testo

\- \*\*Primario:\*\* `#ffffff` / `#f3f4f6` (white / gray-100)

\- \*\*Secondario:\*\* `#d1d5db` (gray-300) — titoli sezioni, info rilevanti

\- \*\*Terziario:\*\* `#9ca3af` (gray-400) — descrizioni, tagline

\- \*\*Placeholder:\*\* `#6b7280` (gray-500) — campi input vuoti

\- \*\*Link:\*\* `#6366f1` (indigo-500), hover `#818cf8` (indigo-400)



\### Accent (CTA, bottoni primari, toggle attivi)

\- \*\*Default:\*\* indigo 500-600 (`#6366f1` → `#4f46e5`)

\- \*\*Hover:\*\* indigo 600 (`#4f46e5`)

\- \*\*Active:\*\* indigo 700 (`#4338ca`)



\### Bottoni per stato

\- \*\*Verde (approvato/disponibile):\*\* `#22c55e` → hover `#16a34a`

\- \*\*Rosso (rifiutato/errore):\*\* `#ef4444` → hover `#dc2626`

\- \*\*Giallo (pending/avviso):\*\* `#eab308` → hover `#ca8a04`



\### Bordi

\- \*\*Default:\*\* `#4b5563` (gray-600)

\- \*\*Input focus:\*\* `#6366f1` (indigo-500) + ring

\- \*\*Separatori:\*\* `#374151` (gray-700), `#4b5563` (gray-600)



\### Gradiente brand

\- \*\*Testo brand "Overseerr":\*\* `#818cf8 → #c084fc` (indigo → purple, background-clip text, trasparente)

\- \*\*Sidebar:\*\* gradiente `#1f2937 → #131928`



\### Scrollbar

\- \*\*Track:\*\* `#1f2937`

\- \*\*Thumb:\*\* `#4b5563`, hover `#6b7280`

\- \*\*Spessore:\*\* 10px



\---



\## Tipografia



\- \*\*Font:\*\* Inter Variable (variabile, peso 100-900) — fallback: `ui-sans-serif, system-ui, sans-serif, Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji`

\- \*\*Titolo pagina (h1):\*\* 2.25rem / font-extrabold (900)

\- \*\*Titolo sezione:\*\* 1.5rem / font-bold (700)

\- \*\*Sottotitoli:\*\* 1.25rem / font-semibold (600)

\- \*\*Corpo:\*\* 0.875rem — 1rem

\- \*\*Etichette/form:\*\* 0.875rem / font-bold

\- \*\*Badge/info piccole:\*\* 0.75rem

\- \*\*Codice:\*\* `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas` con background `#1f2937` e padding 0.25rem 0.5rem



\---



\## Layout



\### Struttura pagine

```

+-----------------------------------------------+

| SIDEBAR (16rem)    |    CONTENUTO PRINCIPALE  |

| - Logo / brand     |    - Header ricerca      |

| - Nav:             |    - Slider orizzontali  |

|   -                |      (card film/serie)   |

|   - Film           |    - Griglie risultati   |

|   - Serie          |    - Dettaglio media     |

+-----------------------------------------------+

```



\- \*\*Sidebar:\*\* `width: 16rem` (lg: `ml-64`), bordo destro `#374151`, gradient sfondo

\- \*\*Responsive:\*\* sidebar collassa su mobile, menu hamburger

\- \*\*Cards orizzontali:\*\* `grid-template-columns: repeat(auto-fill, minmax(16.5rem, 1fr))`

\- \*\*Cards verticali (media thumbnails):\*\* `grid-template-columns: repeat(auto-fill, minmax(9.375rem, 1fr))`



\### Media page (dettaglio film/serie)

```

+---------------------------------------------------+

| \[Background cover immagine]                        |

| +------+  +------------------------------------+  |

| |Poster|  | Titolo (Anno)                       |  |

| | 8rem |  | Attributi e badge                  |  |

| |  ->  |  | Bottoni azione (Richiedi, Play...) |  |

| | 13rem|  +------------------------------------+  |

| +------+                                          |

|                                                    |

| Overview (sinistra)         | Facts panel (destra) |

| - Tagline                   | - Studio             |

| - Trama                     | - Data uscita        |

| - Cast \& crew grid          | - Budget/Incassi     |

| - Slider simili/recommended | - Rating: TMDB, RT   |

+----------------------------------------------------+

```



\---



\## Componenti UI principali



\### Sidebar

\- Gradiente `#1f2937 → #131928`

\- Icone inline + label testo

\- Dropdown utente in basso con quota richieste rimanenti



\### Card Film/Serie (TitleCard)

\- Poster thumbnail (aspect-ratio 2:3 circa)

\- Hover: scala 1.05, overlay info titolo

\- Badge stato (disponibile, pending, approvato, 4K)



\### Slider (carosello orizzontale)

\- Titolo sezione + link "vedi tutto"

\- Scroll overflow-x con nascondi scrollbar

\- Cards in fila, gap 1rem







\### Form controls

\- Input: border `#6b7280`, bg `#374151`, text white, focus ring indigo

\- Toggle switch: bg gray-600 → indigo-500, knob bianco animato

\- Select: custom arrow SVG, bg `#374151`

\- React-Select: tema scuro custom con bg `#374151`, menu `#374151`, opzioni focus `#4b5563`



\---



\## Stati visivi



\### Disponibilità media

| Stato | Colore bordo/badge |

|---|---|

| Disponibile | `#22c55e` (green-500) |

| Parzialmente disponibile | `#eab308` (yellow-500) |

| In elaborazione | `#3b82f6` (blue-500) |

| Richiesta in sospeso | `#f97316` (orange-500) |

| Non disponibile | Nessun badge |







\---



\## Note tecniche



\- \*\*Framework:\*\* Next.js (React) con Tailwind CSS v3.4

\- \*\*Tema:\*\* nativamente dark, nessuna light mode disponibile (prefers-color-scheme non supportata)

\- \*\*Cache immagini:\*\* opzionale, immagini proxy da TMDB/TVDB

\- \*\*Provider icone:\*\* Heroicons (via SVG inline)

\- \*\*Toast:\*\* finestre di notifica 360px width, bottom-right

\- \*\*Media queries breakpoint:\*\* sm:640px, md:768px, lg:1024px, xl:1280px, 2xl:1536px



\---

