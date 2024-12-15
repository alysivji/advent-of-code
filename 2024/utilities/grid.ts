export class Point {
  constructor(
    public x: number,
    public y: number,
  ) {}

  toString() {
    return `${this.x},${this.y}`;
  }

  static fromString(pointStr: string) {
    const parts = pointStr.split(",");
    return new Point(Number(parts[0]), Number(parts[1]));
  }

  add(vector: Vector) {
    return new Point(this.x + vector.xDiff, this.y + vector.yDiff);
  }

  equals(other: Point) {
    return this.x === other.x && this.y === other.y;
  }

  eightDirections() {
    return ALL_DIRECTIONS.map(
      (v) => new Point(this.x + v.xDiff, this.y + v.yDiff),
    );
  }
}

export class Vector {
  constructor(
    public xDiff: number,
    public yDiff: number,
  ) {}

  multiply(scaler: number) {
    return new Vector(scaler * this.xDiff, scaler * this.yDiff);
  }
}

export const ALL_DIRECTIONS = [
  new Vector(0, 1),
  new Vector(1, 1),
  new Vector(1, 0),
  new Vector(1, -1),
  new Vector(0, -1),
  new Vector(-1, -1),
  new Vector(-1, 0),
  new Vector(-1, 1),
];

export const DIAGONALS = [
  new Vector(1, 1),
  new Vector(-1, -1),
  new Vector(1, -1),
  new Vector(-1, 1),
];

export class GridMap {
  private _map: Map<string, string>;

  constructor() {
    this._map = new Map();
  }

  set(point: Point, value: string) {
    return this._map.set(point.toString(), value);
  }

  get(point: Point) {
    return this._map.get(point.toString());
  }

  has(point: Point) {
    return this._map.has(point.toString());
  }

  entries() {
    return this._map.entries();
  }

  neighbours8Directions(point: Point) {
    return point.eightDirections().filter((p) => this.has(p));
  }
}

export class GridSet {
  private _set: Set<string>;

  constructor(points: Point[] = []) {
    this._set = new Set();
    points.forEach((point) => this.add(point));
  }

  get size() {
    return this._set.size;
  }

  add(point: Point) {
    this._set.add(point.toString());
  }

  has(point: Point) {
    return this._set.has(point.toString());
  }

  delete(point: Point) {
    return this._set.delete(point.toString());
  }

  // TODO make this into an iterator
  values() {
    return this._set.values();
  }
}
