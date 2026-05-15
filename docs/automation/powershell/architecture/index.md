# PowerShell — Architecture

<div class="kb-summary">
Cross-platform automation shell on .NET; execution engine processes input through parser → AST → runspace → pipeline; remoting via WinRM (5985/5986) or SSH; module system with PSGallery distribution; runspace pools for parallelism.
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Execution engine, pipeline, remoting (WinRM/SSH), module system, and runspace model.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## PowerShell Core vs Windows PowerShell

| Attribute | Windows PowerShell | PowerShell 7+ |
|---|---|---|
| Runtime | .NET Framework 4.x | .NET 6 / 7 / 8 (cross-platform) |
| Platforms | Windows only | Windows, Linux, macOS |
| Version | 5.1 (final) | 7.x (active development) |
| Remoting | WinRM only | WinRM + SSH |
| Release cadence | Security patches only | Active feature releases |

## Execution Engine

```mermaid
flowchart LR
    A([Input<br/>stdin / script / command]) --> B[Lexer & Parser]
    B --> C[AST\nAbstract Syntax Tree]
    C --> D[Binder\nType resolution]
    D --> E[Compiled Script Block]
    E --> F{Runspace}
    F --> G[Command Discovery\nAlias → Function → Cmdlet → Native]
    G --> H[Parameter Binding]
    H --> I[Pipeline Processor]
    I --> J[Output / Objects]
    J --> K([stdout / next cmdlet / $null])
    I --> L([Error Stream\n$Error / Write-Error])
    style F fill:#1565c0,color:#fff
    style I fill:#2e7d32,color:#fff
```
