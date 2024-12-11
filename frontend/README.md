# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

https://github.com/phillipdupuis/pydantic-to-typescript
https://www.saraui.com/

data persitance :
https://www.reddit.com/r/sveltejs/comments/177dzhg/sharing_data_between_routes_on_server_in_static/
https://sveltequery.vercel.app/

route protection:
https://stackoverflow.com/questions/70271307/how-do-i-make-a-protected-route-handler-for-svelte-kit-using-static-adapter
https://github.com/MathieuDoyon/svelte-kit-static-protected-route

form validation
https://svelte.dev/playground/b9a5d3829c77437bb548c3aafbe5cd5c?version=3.32.3

```bash
pip install 'pydantic-to-typescript>=2'
pip install pydantic-extra-types
npm i json-schema-to-typescript

pydantic2ts --module ./app/books.py --output ./frontend/src/lib/apiTypes.ts
pydantic2ts --module ./backend/models.py --exclude SQLModelBaseUserDB --exclude User --output ./frontend/src/lib/apiTypes.ts
```

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
