export 'utilities.dart';

class Point {
  int x;
  int y;

  Point east() {
    return this + Vector(1, 0);
  }

  Point north() {
    return this + Vector(0, -1);
  }

  Point south() {
    return this + Vector(0, 1);
  }

  Point west() {
    return this + Vector(-1, 0);
  }

  Iterable<Point> adjacent8() {
    List<Vector> vectors = [
      Vector(-1, 0),
      Vector(1, 0),
      Vector(0, 1),
      Vector(0, -1),
      Vector(1, 1),
      Vector(1, -1),
      Vector(-1, 1),
      Vector(-1, -1),
    ];

    return vectors.map((vector) => this + vector);
  }

  Point operator +(Vector vector) {
    return Point(x + vector.xDiff, y + vector.yDiff);
  }

  @override
  bool operator ==(Object other) {
    if (other is! Point) return false;
    if (x != other.x) return false;
    if (y != other.y) return false;
    return true;
  }

  @override
  int get hashCode => Object.hash(x, y);

  @override
  String toString() {
    return "$x, $y";
  }

  Point(this.x, this.y);
}

class Vector {
  int xDiff;
  int yDiff;

  Vector(this.xDiff, this.yDiff);
}
