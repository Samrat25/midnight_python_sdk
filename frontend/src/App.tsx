import { buttonVariants } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import ShinyText from "@/components/ShinyText"
import SpotlightCard from "@/components/SpotlightCard"
import {
  ArrowDown,
  ArrowRight,
  BookOpen,
  Github,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  Lock,
  Workflow,
  Code2,
  Zap,
  type LucideIcon,
} from "lucide-react"
import { lazy, Suspense } from "react"

const Silk = lazy(() => import("@/components/Silk"))

type Feature = {
  icon: LucideIcon
  title: string
  description: string
}

type GuideStep = {
  step: string
  title: string
  description: string
  note: string
}

type CodePanelProps = {
  label: string
  title: string
  code: string
  className?: string
}

type IconLinkProps = {
  href: string
  icon: LucideIcon
  label: string
  className?: string
}

const heroBullets = [
  "Privacy-first blockchain development",
  "Zero-knowledge proof integration",
  "Compact language smart contracts",
  "Python SDK for seamless integration",
]

const helperRoutes = [
  "deploy_contract()",
  "create_wallet()",
  "submit_transaction()",
  "query_state()",
  "verify_proof()",
]

const features: Feature[] = [
  {
    icon: ShieldCheck,
    title: "Privacy by design",
    description:
      "Build applications with built-in privacy using zero-knowledge proofs and shielded state management.",
  },
  {
    icon: Lock,
    title: "Secure smart contracts",
    description:
      "Write contracts in Compact, a type-safe language designed specifically for privacy-preserving applications.",
  },
  {
    icon: Code2,
    title: "Python SDK integration",
    description:
      "Seamlessly integrate Midnight blockchain into your Python applications with our comprehensive SDK.",
  },
  {
    icon: Workflow,
    title: "Complete development flow",
    description:
      "From contract deployment to transaction submission, manage your entire blockchain workflow with ease.",
  },
]

const guideSteps: GuideStep[] = [
  {
    step: "01",
    title: "Install the SDK",
    description:
      "Install the Midnight Python SDK using pip or your preferred package manager to get started.",
    note: "Start with the package command below, then move into your Python application.",
  },
  {
    step: "02",
    title: "Create a wallet",
    description:
      "Initialize a wallet instance to manage your Midnight blockchain interactions and transactions.",
    note: "You can create a new wallet or import an existing one using a mnemonic phrase.",
  },
  {
    step: "03",
    title: "Deploy your contract",
    description:
      "Compile your Compact smart contract and deploy it to the Midnight network using the SDK.",
    note: "The SDK handles contract compilation, deployment, and initialization automatically.",
  },
  {
    step: "04",
    title: "Submit transactions",
    description:
      "Interact with your deployed contracts by submitting transactions with zero-knowledge proofs.",
    note: "The SDK manages proof generation and transaction signing for you.",
  },
  {
    step: "05",
    title: "Query contract state",
    description:
      "Read public and private state from your contracts using the query methods provided by the SDK.",
    note: "Access both shielded and public data with type-safe interfaces.",
  },
  {
    step: "06",
    title: "Monitor transactions",
    description:
      "Track transaction status and listen for events emitted by your smart contracts.",
    note: "The SDK provides async methods for real-time transaction monitoring.",
  },
]

const paymentFlow = [
  "Write your smart contract in Compact language.",
  "Deploy the contract to Midnight network using the SDK.",
  "Submit transactions with zero-knowledge proofs.",
  "Query contract state and verify proofs on-chain.",
]

const installCode = `pip install midnight-sdk

# From source
git clone 
cd midnight-sdk
pip install -e .`

const quickStartCode = `from midnight_sdk import MidnightSDK, Wallet

# Initialise https://github.com/Samrat25/midnight_python_sdk SDK
sdk = MidnightSDK(network="testnet")

# Create or import wallet
wallet = Wallet.create()
# or
wallet = Wallet.from_mnemonic("your mnemonic phrase")

# Deploy contract
contract = sdk.deploy_contract(
    contract_path="./contracts/my_contract.compact",
    wallet=wallet
)

# Submit transaction
tx = contract.submit_transaction(
    method="transfer",
    args={"amount": 100, "recipient": "address"},
    wallet=wallet
)

print(f"Transaction hash: {tx.hash}")`

const contractCode = `circuit MyContract {
  // Private state
  private field balance;
  
  // Public state
  public field totalSupply;
  
  // Constructor
  constructor(field initial) {
    balance = initial;
    totalSupply = initial;
  }
  
  // Transfer with ZK proof
  public transfer(field amount) {
    require(balance >= amount);
    balance = balance - amount;
  }
}`

const queryCode = `# Query contract state
public_state = contract.query_public_state()
print(f"Total supply: {public_state.totalSupply}")

# Query with proof
private_state = contract.query_private_state(
    wallet=wallet
)
print(f"Balance: {private_state.balance}")`

const resourceLinks: IconLinkProps[] = [
  {
    href: "https://docs.midnight.network",
    icon: BookOpen,
    label: "Documentation",
    className:
      "border-[#4a3aff]/35 text-[#a68eff] hover:bg-[#4a3aff]/16 hover:text-white",
  },
  {
    href: "https://github.com/Samrat25/midnight_python_sdk",
    icon: Github,
    label: "GitHub",
    className:
      "border-[#7c5cff]/35 text-[#c9b3ff] hover:bg-[#7c5cff]/16 hover:text-white",
  },
]

function IconLink({ href, icon: Icon, label, className }: IconLinkProps) {
  return (
    <a
      aria-label={label}
      className={cn(
        "flex size-11 items-center justify-center rounded-full border bg-white/8 text-white/72 transition",
        className,
      )}
      href={href}
      rel="noreferrer"
      target="_blank"
      title={label}
    >
      <Icon className="size-4.5" />
    </a>
  )
}

function SectionHeading({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string
  title: string
  description: string
}) {
  return (
    <div className="max-w-3xl">
      <p className="text-sm font-semibold uppercase tracking-[0.28em] text-[#a68eff]">
        {eyebrow}
      </p>
      <h2 className="mt-4 font-heading text-4xl leading-tight text-white sm:text-5xl">
        {title}
      </h2>
      <p className="mt-5 text-lg leading-8 text-white/72">{description}</p>
    </div>
  )
}

function CodePanel({ label, title, code, className }: CodePanelProps) {
  return (
    <SpotlightCard
      spotlightColor="rgba(74, 58, 255, 0.12)"
      className={cn(
        "overflow-hidden rounded-[2rem] border-white/12 bg-[#0e0e1a]/92 text-white",
        className,
      )}
    >
      <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-white/45">
            {label}
          </p>
          <h3 className="mt-2 text-lg font-semibold text-white">{title}</h3>
        </div>
        <div className="flex items-center gap-2">
          <span className="size-2.5 rounded-full bg-[#a68eff]" />
          <span className="size-2.5 rounded-full bg-[#c9b3ff]" />
          <span className="size-2.5 rounded-full bg-[#7c5cff]" />
        </div>
      </div>
      <pre className="overflow-x-auto px-5 py-5 text-sm leading-7 text-white/86">
        <code>{code}</code>
      </pre>
    </SpotlightCard>
  )
}

function App() {
  return (
    <main id="top" className="relative min-h-screen overflow-x-hidden text-white">
      <div className="fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute inset-0">
          <Suspense
            fallback={
              <div className="h-full w-full bg-[#1a1a2e]" />
            }
          >
            <Silk
              speed={5}
              scale={1}
              color="#1a1a2e"
              noiseIntensity={1.4}
              rotation={0}
            />
          </Suspense>
        </div>
      </div>

      <div className="relative z-10">
        <header className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-6 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <div className="flex items-center gap-3">
            <div className="rounded-full border border-white/15 bg-white/8 px-4 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-white/75 backdrop-blur-md">
              Midnight SDK
            </div>
            <span className="hidden text-sm text-white/55 sm:inline">
              Privacy-preserving blockchain development
            </span>
          </div>

          <div className="flex items-center gap-4">
            <nav className="flex flex-wrap items-center gap-3 text-sm text-white/70">
              <a className="transition hover:text-white" href="#modules">
                Features
              </a>
              <a className="transition hover:text-white" href="#build">
                Build
              </a>
              <a className="transition hover:text-white" href="#flow">
                Flow
              </a>
            </nav>
            <div className="flex items-center gap-2">
              {resourceLinks.map((link) => (
                <IconLink key={link.label} {...link} />
              ))}
            </div>
          </div>
        </header>

        <section className="mx-auto max-w-7xl px-6 pb-24 pt-14 lg:px-10">
          <div className="grid gap-12 lg:grid-cols-[1.1fr_0.9fr] lg:items-end">
            <div className="max-w-3xl">
              <div className="inline-flex flex-wrap items-center gap-2 rounded-full border border-white/12 bg-white/8 px-4 py-2 text-sm text-white/72 backdrop-blur-md">
                <Sparkles className="size-4 text-[#a68eff]" />
                <ShinyText
                  className="font-medium tracking-[0.02em]"
                  color="#c9b3ff"
                  delay={0}
                  direction="left"
                  shineColor="#ffffff"
                  speed={2}
                  spread={120}
                  text="Privacy-first blockchain development"
                />
              </div>

              <h1 className="mt-7 font-heading text-5xl leading-[0.95] text-white sm:text-6xl lg:text-7xl">
                Build privacy-preserving applications on Midnight blockchain.
              </h1>

              <p className="mt-6 max-w-2xl text-lg leading-8 text-white/76 sm:text-xl">
                Midnight SDK provides everything you need to build, deploy, and interact with
                privacy-preserving smart contracts using zero-knowledge proofs and the Compact
                language.
              </p>

              <div className="mt-8 flex flex-wrap gap-4">
                <a
                  className={cn(
                    buttonVariants({ size: "lg" }),
                    "h-11 rounded-full px-5 text-sm font-semibold shadow-[0_20px_60px_rgba(74,58,255,0.28)]",
                  )}
                  href="#build"
                >
                  Scroll to build
                  <ArrowDown className="size-4" />
                </a>
                <a
                  className={cn(
                    buttonVariants({ variant: "outline", size: "lg" }),
                    "h-11 rounded-full border-white/15 bg-white/8 px-5 text-sm text-white hover:bg-white/14 hover:text-white",
                  )}
                  href="#modules"
                >
                  Explore features
                  <ArrowRight className="size-4" />
                </a>
              </div>

              <div className="mt-10 grid gap-3 sm:grid-cols-2">
                {heroBullets.map((bullet) => (
                  <SpotlightCard
                    key={bullet}
                    className="rounded-[1.5rem] border-white/10 bg-white/8 px-4 py-4 text-sm text-white/80"
                    spotlightColor="rgba(166, 142, 255, 0.12)"
                  >
                    {bullet}
                  </SpotlightCard>
                ))}
              </div>
            </div>

            <div className="grid gap-5">
              <SpotlightCard
                className="rounded-[2rem] border-white/12 bg-white/10 p-6"
                spotlightColor="rgba(74, 58, 255, 0.14)"
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.28em] text-white/45">
                      Powerful features
                    </p>
                    <h2 className="mt-2 text-2xl font-semibold text-white">
                      One SDK, complete privacy-preserving toolkit.
                    </h2>
                  </div>
                  <div className="rounded-2xl border border-white/12 bg-white/8 p-3">
                    <TerminalSquare className="size-6 text-[#a68eff]" />
                  </div>
                </div>

                <div className="mt-5 space-y-3">
                  {features.slice(0, 3).map((feature) => (
                    <SpotlightCard
                      key={feature.title}
                      className="rounded-[1.35rem] border-white/10 bg-black/18 px-4 py-4"
                      spotlightColor="rgba(166, 142, 255, 0.1)"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex size-10 items-center justify-center rounded-2xl bg-[#4a3aff]/18 text-[#c9b3ff]">
                          <feature.icon className="size-5" />
                        </div>
                        <div>
                          <p className="text-sm font-semibold text-white">
                            {feature.title}
                          </p>
                          <p className="mt-1 text-sm leading-6 text-white/66">
                            {feature.description}
                          </p>
                        </div>
                      </div>
                    </SpotlightCard>
                  ))}
                </div>
              </SpotlightCard>

              <SpotlightCard
                className="rounded-[2rem] border-white/12 bg-black/20 p-6"
                spotlightColor="rgba(74, 58, 255, 0.12)"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.28em] text-white/45">
                  Where the practical setup lives
                </p>
                <h2 className="mt-2 text-2xl font-semibold text-white">
                  Installation and contract examples sit below the fold.
                </h2>
                <p className="mt-4 text-[15px] leading-7 text-white/72">
                  The homepage stays product-first. Scroll down for the install
                  commands, Python examples, contract deployment, and the
                  normal path for building privacy-preserving applications.
                </p>
              </SpotlightCard>
            </div>
          </div>
        </section>

        <section
          id="modules"
          className="mx-auto max-w-7xl px-6 py-20 lg:px-10"
        >
          <div className="rounded-[2.5rem] border border-white/10 bg-white/5 p-6 backdrop-blur-xl sm:p-8">
            <SectionHeading
              eyebrow="Features"
              title="A comprehensive SDK for privacy-preserving development."
              description="Each part of the SDK has a clear purpose: contract deployment, wallet management, transaction submission, state queries, and zero-knowledge proof verification."
            />

            <div className="mt-12 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
              {features.map((feature) => (
                <SpotlightCard
                  key={feature.title}
                  className="rounded-[2rem] border-white/10 bg-[#1e1e3a]/90 p-6 text-white backdrop-blur-sm"
                  spotlightColor="rgba(74, 58, 255, 0.14)"
                >
                  <div className="flex size-12 items-center justify-center rounded-2xl bg-[#4a3aff]/20 text-[#a68eff]">
                    <feature.icon className="size-5" />
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-white">{feature.title}</h3>
                  <p className="mt-4 text-[15px] leading-7 text-white/70">
                    {feature.description}
                  </p>
                </SpotlightCard>
              ))}
            </div>

            <div className="mt-6 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <SpotlightCard
                className="rounded-[2.25rem] border-white/10 bg-[#1e1e3a]/90 p-6 text-white backdrop-blur-sm"
                spotlightColor="rgba(166, 142, 255, 0.18)"
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#a68eff]">
                      SDK methods
                    </p>
                    <h3 className="mt-3 text-2xl font-semibold text-white">
                      Python SDK provides intuitive methods for all operations.
                    </h3>
                  </div>
                  <div className="rounded-2xl bg-[#4a3aff]/20 p-3 text-[#a68eff]">
                    <Zap className="size-6" />
                  </div>
                </div>

                <div className="mt-6 grid gap-4 md:grid-cols-2">
                  <div className="rounded-[1.5rem] border border-white/10 bg-[#2a2a4a]/60 p-4">
                    <p className="text-sm font-semibold text-white">Contract operations</p>
                    <p className="mt-2 text-sm leading-6 text-white/70">
                      Deploy contracts, submit transactions, and query state with
                      type-safe Python interfaces.
                    </p>
                  </div>
                  <div className="rounded-[1.5rem] border border-white/10 bg-[#2a2a4a]/60 p-4">
                    <p className="text-sm font-semibold text-white">Wallet management</p>
                    <p className="mt-2 text-sm leading-6 text-white/70">
                      Create wallets, manage keys, and sign transactions with
                      built-in security features.
                    </p>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap gap-3">
                  {helperRoutes.map((route) => (
                    <span
                      key={route}
                      className="rounded-full border border-white/10 bg-[#2a2a4a]/60 px-3 py-2 text-sm text-[#c9b3ff]"
                    >
                      {route}
                    </span>
                  ))}
                </div>
              </SpotlightCard>

              <SpotlightCard
                id="flow"
                className="rounded-[2.25rem] border-white/10 bg-[#1e1e3a]/90 p-6 text-white backdrop-blur-sm"
                spotlightColor="rgba(74, 58, 255, 0.16)"
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.28em] text-[#a68eff]">
                      Development flow
                    </p>
                    <h3 className="mt-3 text-2xl font-semibold text-white">
                      From contract to deployment in four simple steps.
                    </h3>
                  </div>
                  <div className="rounded-2xl bg-[#4a3aff]/20 p-3 text-[#a68eff]">
                    <Workflow className="size-6" />
                  </div>
                </div>

                <div className="mt-6 space-y-3">
                  {paymentFlow.map((item, index) => (
                    <SpotlightCard
                      key={item}
                      className="flex gap-4 rounded-[1.35rem] border border-white/10 bg-[#2a2a4a]/60 px-4 py-4"
                      spotlightColor="rgba(74, 58, 255, 0.12)"
                    >
                      <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-[#4a3aff] text-sm font-semibold text-white">
                        {index + 1}
                      </div>
                      <p className="text-sm leading-7 text-white/70">{item}</p>
                    </SpotlightCard>
                  ))}
                </div>
              </SpotlightCard>
            </div>
          </div>
        </section>

        <section id="build" className="mx-auto max-w-7xl px-6 py-20 lg:px-10">
          <div className="rounded-[2.5rem] border border-white/10 bg-white/5 p-6 backdrop-blur-xl sm:p-8">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
              <SectionHeading
                eyebrow="Build"
                title="Install the SDK and deploy your first privacy-preserving contract."
                description="Everything practical lives here: installation, wallet setup, contract deployment, transaction submission, and state queries for building on Midnight."
              />
              <div className="flex items-center gap-2">
                {resourceLinks.map((link) => (
                  <IconLink key={`${link.label}-build`} {...link} />
                ))}
              </div>
            </div>

            <div className="mt-12 grid gap-12 lg:grid-cols-[0.9fr_1.1fr]">
              <div className="space-y-4">
                {guideSteps.map((item) => (
                  <SpotlightCard
                    key={item.step}
                    className="rounded-[1.75rem] border-white/10 bg-[#1e1e3a]/90 p-5 text-white backdrop-blur-sm"
                    spotlightColor="rgba(74, 58, 255, 0.16)"
                  >
                    <div className="flex gap-4">
                      <div className="flex size-11 shrink-0 items-center justify-center rounded-full bg-[#4a3aff] text-sm font-semibold text-white">
                        {item.step}
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-white">{item.title}</h3>
                        <p className="mt-2 text-[15px] leading-7 text-white/70">
                          {item.description}
                        </p>
                        <p className="mt-3 text-sm leading-6 text-[#a68eff]">
                          {item.note}
                        </p>
                      </div>
                    </div>
                  </SpotlightCard>
                ))}
              </div>

              <div className="space-y-6">
                <CodePanel
                  label="Install"
                  title="Package installation"
                  code={installCode}
                />
                <CodePanel
                  label="Python"
                  title="Quick start example"
                  code={quickStartCode}
                />
                <div className="grid gap-6 xl:grid-cols-2">
                  <CodePanel
                    label="Compact"
                    title="Smart contract"
                    code={contractCode}
                  />
                  <CodePanel
                    label="Query"
                    title="Read contract state"
                    code={queryCode}
                  />
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}

export default App
