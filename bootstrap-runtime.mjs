
import { initializeRuntime } from './semantic-runtime/loader/runtime-loader.mjs'

const runtime = await initializeRuntime({
  runtimeClass: 'nnbryo-continuity-runtime'
})

await runtime.bootstrap()
