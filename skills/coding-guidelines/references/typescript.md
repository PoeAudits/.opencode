# TypeScript Coding Guidelines

TypeScript-specific coding standards for writing strict, idiomatic TypeScript. Consult this reference before writing any TypeScript or JavaScript code. These rules supplement the general coding principles in the parent skill.

---

## Architecture & Design Patterns

- Prefer functional style unless multiple instances of the same object type are needed.
- Prefer composition and interfaces over abstract classes and inheritance.
- Keep functions small, well-contained, and single-purpose — each function does one thing well.

## Interfaces vs Types

Use `interface` for object shapes — if it can be an interface, it MUST be an interface.
Use `type` for unions, intersections, and mapped types.

```typescript
// Good - object shape
interface User {
  id: string;
  name: string;
}

// Good - union type
type Status = "pending" | "active" | "inactive";

// Good - intersection
type AdminUser = User & { permissions: string[] };
```

## Type System

- **Strict Mode:** Always use `strict: true` in tsconfig (including `strictNullChecks`).
- **No `any`:** Never use `any` except in extreme circumstances; everything MUST be strictly typed.
- **Type Guards:** Prefer type guards over `as Type` assertions.

```typescript
// Good - type guard
function isUser(obj: unknown): obj is User {
  return typeof obj === "object" && obj !== null && "id" in obj;
}

// Avoid - type assertion
const user = data as User;
```

- **Explicit Return Types:** Always annotate function return types explicitly.
- **Type-Only Imports:** Use `import type` for types to improve build performance and clarify intent.

```typescript
// Good - type-only import
import type { User, UserConfig } from "./types";
import { createUser } from "./user";

// Avoid - mixing types with runtime imports when separable
import { User, UserConfig, createUser } from "./user";
```

## Advanced Type Patterns

**Branded Types:** Use branded types for domain modeling to prevent primitive type confusion.

```typescript
type UserId = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };

function createUserId(id: string): UserId {
  return id as UserId;
}

// Compiler prevents mixing UserId and OrderId
function getUser(id: UserId): User { /* ... */ }
getUser(orderId); // Error: OrderId not assignable to UserId
```

**Discriminated Unions:** Use discriminated unions for state machines and variant types.

```typescript
type RequestState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: User }
  | { status: "error"; error: Error };

function handleState(state: RequestState): void {
  switch (state.status) {
    case "idle":
      return;
    case "loading":
      showSpinner();
      return;
    case "success":
      displayUser(state.data); // TypeScript knows data exists
      return;
    case "error":
      showError(state.error); // TypeScript knows error exists
      return;
  }
}
```

**Exhaustive Checking:** Use the `never` type to ensure all cases are handled.

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

function handleStatus(status: Status): string {
  switch (status) {
    case "pending":
      return "Waiting...";
    case "active":
      return "Running";
    case "inactive":
      return "Stopped";
    default:
      return assertNever(status); // Compile error if case is missing
  }
}
```

**Const Assertions:** Use `as const` for literal types and immutable data.

```typescript
// Creates readonly tuple with literal types
const ROLES = ["admin", "user", "guest"] as const;
type Role = (typeof ROLES)[number]; // "admin" | "user" | "guest"

// Creates deeply readonly object with literal types
const CONFIG = {
  api: { timeout_ms: 5000, retries_max: 3 },
  features: { darkMode: true },
} as const;
```

**Satisfies Operator:** Use `satisfies` to validate types while preserving inference.

```typescript
type RouteConfig = Record<string, { path: string; auth: boolean }>;

// Validates structure but preserves literal types
const routes = {
  home: { path: "/", auth: false },
  dashboard: { path: "/dashboard", auth: true },
} satisfies RouteConfig;

// TypeScript knows exact keys: routes.home, routes.dashboard
// Not just: routes[string]
```

**Const Enums:** Use `const enum` only when inlined values are needed and the entire codebase is controlled.

```typescript
// Good - when zero runtime overhead is needed and not publishing as library
const enum HttpStatus {
  OK = 200,
  NOT_FOUND = 404,
  SERVER_ERROR = 500,
}
// Compiles to: if (status === 200) instead of: if (status === HttpStatus.OK)

// Avoid const enum when:
// - Publishing a library (consumers cannot use --isolatedModules)
// - Using --isolatedModules (const enums do not work)
// - Runtime iteration over enum values is needed

// Prefer union types for most cases (see Enums section)
```

## Build Optimization

**Project References:** Use project references for large codebases to enable incremental builds.

```json
// tsconfig.json
{
  "compilerOptions": {
    "composite": true,
    "incremental": true,
    "tsBuildInfoFile": "./dist/.tsbuildinfo"
  },
  "references": [
    { "path": "./packages/shared" },
    { "path": "./packages/api" }
  ]
}
```

Build with `tsc --build` to leverage incremental compilation.

**Incremental Compilation:** Enable incremental builds for faster compilation.

```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": "./dist/.tsbuildinfo"
  }
}
```

**Skip Lib Check:** Use `skipLibCheck: true` to speed up compilation (skips type checking of declaration files).

## Null Handling

- Prefer `undefined` over `null` for absent values (aligns with TypeScript's optional property behavior).
- Use explicit null checks over optional chaining for clarity.

```typescript
// Preferred - explicit check
if (user !== undefined) {
  console.log(user.name);
}

// Avoid when possible
console.log(user?.name);
```

- **Nullish Coalescing:** Use `??` over `||` for defaults when dealing with potentially falsy values.

## Enums

Prefer union types over TypeScript `enum` (avoids runtime quirks).

```typescript
// Good - union type
type Status = "pending" | "active" | "inactive";

// Avoid - enum
enum Status {
  Pending,
  Active,
  Inactive,
}
```

## Code Style

- **Semicolons:** Use semicolons.
- **Quotes:** Use double quotes for strings; use single quotes only when the string contains double quotes.
- **Naming Conventions:**
  - `camelCase` for variables, functions, methods
  - `PascalCase` for classes, interfaces, types, enums
  - `UPPER_SNAKE_CASE` for constants
- **File Naming:** `kebab-case.ts` for files, `PascalCase.ts` for files exporting a single class/component.

## Comments & Documentation

- Keep comments minimal or omit entirely.
- Use JSDoc for public APIs when documentation is needed.
- Let type annotations document function signatures.

## Modules & Imports

- **Named Imports:** Always use named imports; avoid `import *`.

```typescript
// Good
import { UserService, UserRepository } from "./user";

// Avoid
import * as User from "./user";
```

- **Barrel Files:** Use `index.ts` re-exports only where they provide clear organizational benefit.
- **Default vs Named Exports:** Named exports are generally preferred for better refactoring support.
- **Path Aliases:** Use `@/` style imports for cleaner paths (configure in tsconfig `paths`).

```typescript
// Good - path alias
import { UserService } from "@/services/user";

// Also acceptable - relative
import { UserService } from "../../services/user";
```

## Error Handling

- **Custom Errors:** Create custom error classes, typically in their own file.

```typescript
// errors.ts
export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ValidationError";
  }
}
```

- **Exceptions:** Use throw/catch for error handling (not Result/Either pattern).

## Async

- Prefer `async/await` over raw Promises for readability.
- Use raw Promises only when best practices dictate (e.g., `Promise.all` for concurrent operations).

## Testing

- **Framework:** Use Bun's built-in test runner for Bun projects; use Vitest or Jest for pnpm/Node projects (whichever is most common for the project type).
- **Organization:** Keep tests in a separate `tests/` directory (not colocated with source).
- **Structure:** Mirror source directory structure within tests.

## Tooling

- **Linter/Formatter:** Use ESLint + Prettier.
- **Runtime:** Prefer Bun; use Node.js when project requirements dictate.

## Dependency Management

- Use Bun or pnpm package manager — always check which package manager the project uses.
- Avoid adding new packages unless necessary.
- Use lockfiles (`bun.lockb`, `pnpm-lock.yaml`).

## Security

- Never commit or log secrets, API keys, or credentials.
- Use environment variables for sensitive configuration.

## React & Next.js

- **Components:** Use functional components only; avoid class components.
- **Hooks:** Prefer hooks over HOCs (Higher-Order Components).
- **Styling:** Use Tailwind CSS for styling.

```typescript
// Good - functional component with hooks
function UserProfile({ userId }: UserProfileProps): JSX.Element {
  const [user, setUser] = useState<User | undefined>(undefined);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  return <div className="p-4 bg-white rounded-lg">{user?.name}</div>;
}
```

## Runtime Validation

Use Zod for runtime validation of external data (API responses, form inputs, environment variables).

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  age: z.number().min(0),
});

type User = z.infer<typeof UserSchema>;

// Validate at runtime
const user = UserSchema.parse(apiResponse);
```
