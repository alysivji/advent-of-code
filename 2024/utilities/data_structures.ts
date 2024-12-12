export class Counter<T> {
  private _map: Map<T, number>;

  constructor(iterable: T[]) {
    this._map = new Map();

    for (const item of iterable) {
      this._map.set(item, (this._map.get(item) || 0) + 1);
    }
  }

  sorted(order: "asc" | "desc" = "desc"): [T, number][] {
    const entries = Array.from(this._map.entries());
    return entries.sort((a, b) =>
      order === "asc" ? a[1] - b[1] : b[1] - a[1],
    );
  }
}
