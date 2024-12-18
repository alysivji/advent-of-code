export function* permutations<T>(k: number, A: T[]): Generator<T[]> {
  // https://en.wikipedia.org/wiki/Heap%27s_algorithm

  if (k > A.length) return [];

  if (k === 1) {
    yield A;
    return;
  }

  yield* permutations(k - 1, A);

  for (let i = 0; i < k - 1; i++) {
    if (k % 2 === 0) {
      const tmp = A[i];
      A[i] = A[k - 1];
      A[k - 1] = tmp;
    } else {
      const tmp = A[0];
      A[0] = A[k - 1];
      A[k - 1] = tmp;
    }
    yield* permutations(k - 1, A);
  }
}
