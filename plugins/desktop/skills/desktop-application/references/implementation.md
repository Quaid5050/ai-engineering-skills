# Desktop platform adapters

| Target | Implementation concerns |
|---|---|
| macOS AppKit/SwiftUI | TCC/entitlements, App Sandbox where applicable, signed/notarized distribution, menu/keyboard behavior, accessibility tree, App Groups and protected data |
| Windows WinUI/WPF/Win32 | MSIX or chosen installer, code signing, standard-user/elevation separation, COM/registry scope, UI Automation and update recovery |
| Linux GTK/Qt/native | Supported distributions, Wayland/X11, portal/file permissions, package format, desktop integration and assistive technology |
| Electron | Sandboxed renderers, context isolation, narrow preload IPC, navigation/origin validation and signed updates; renderer content must not receive general Node privileges |
| Tauri | Explicit capabilities/commands, validated IPC arguments, filesystem scope and updater signature verification |
| Qt | QObject/thread affinity, signal lifetime, resource packaging, platform plugins and accessibility |
| .NET MAUI | Platform handler differences, permissions/lifecycle, packaged builds and native accessibility; mobile success is not desktop evidence |

Use current official toolkit/OS documentation for the installed release. Each target starts at documented support until its packaged fixture and OS checks run. No one installer or UI abstraction covers every platform identically.
