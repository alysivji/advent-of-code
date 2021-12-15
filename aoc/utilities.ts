// Advent of Code Toolbox

// TODO add all map functionality to class
export class GridMap {
  _map: Map<string, number>;

  constructor() {
    // TODO take in array and initialize
    this._map = new Map();
  }

  set(point: Array<number>, value: number) {
    const key = point.join(",");
    this._map.set(key, value);
    return this;
  }

  get(point: Array<number>): number | undefined {
    const key = point.join(",");
    return this._map.get(key);
  }

  has(point: Array<number>): boolean {
    const key = point.join(",");
    return this._map.has(key);
  }

  entries() {
    return this._map.entries();
  }
}

export class GridSet {
  // todo copy set methods and return values
  _set: Set<string>;

  constructor() {
    this._set = new Set();
  }

  add(item: number[]) {
    const key = item.join(",");
    this._set.add(key);
  }

  has(item: number[]): boolean {
    const key = item.join(",");
    return this._set.has(key);
  }

  entries() {
    return this._set.entries();
  }

  get size(): number {
    return this._set.size;
  }
}
