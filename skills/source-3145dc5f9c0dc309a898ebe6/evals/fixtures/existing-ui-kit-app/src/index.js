import Resolver from '@forge/resolver';

const resolver = new Resolver();
resolver.define('get-summary', async () => 'Existing summary');

export const handler = resolver.getDefinitions();
