"""Interactive terminal demo for the school note populator."""

from __future__ import annotations

import time

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from service import populate_template

load_dotenv()

console = Console()


def render_note(result) -> None:
    t = result.template
    from datetime import date

    today = date.today().strftime("%B %d, %Y")

    note_body = (
        f"[bold]Date:[/bold] {today}\n"
        f"\n"
        f"[bold]To:[/bold] {t.school_name} Administration\n"
        f"\n"
        f"Dear School Administration,\n"
        f"\n"
        f"Please excuse my child's absence from school.\n"
        f"\n"
        f"[bold]Reason for Absence:[/bold]  {t.reason_for_absence}\n"
        f"[bold]Expected Return:[/bold]     {t.date_of_return}\n"
        f"\n"
        f"Thank you for your understanding.\n"
        f"\n"
        f"Sincerely,\n"
        f"[dim italic]Parent / Guardian[/dim italic]"
    )

    console.print()
    console.print(
        Panel(
            note_body,
            title="[bold]School Absence Note[/bold]",
            border_style="green",
            padding=(1, 4),
            width=60,
        )
    )


CANNED_REPLY = (
    "We can generate a doctor's note for you and send it off to a PCP. "
    "Can you describe why your child needs time off?"
)


def main() -> None:
    console.print(
        Panel(
            "[bold]School Note Populator[/bold]\n"
            "Type [bold red]quit[/bold red] to exit.",
            border_style="blue",
        )
    )

    # --- scripted opening ---
    console.print()
    first_msg = console.input("[bold green]You:[/bold green] ")
    if first_msg.strip().lower() in ("quit", "exit", "q"):
        console.print("\n[dim]Goodbye![/dim]")
        return

    with console.status("Analyzing message..."):
        time.sleep(2)

    with console.status("School absence note detected — preparing template..."):
        time.sleep(1.5)

    console.print(
        Text.from_markup(f"\n[bold cyan]Assistant:[/bold cyan] {CANNED_REPLY}")
    )

    messages: list[str] = [
        f"Parent: {first_msg}",
        f"Assistant: {CANNED_REPLY}",
    ]

    # --- live flow ---
    while True:
        console.print()
        user_input = console.input("[bold green]You:[/bold green] ")
        if user_input.strip().lower() in ("quit", "exit", "q"):
            console.print("\n[dim]Goodbye![/dim]")
            break

        messages.append(f"Parent: {user_input}")
        conversation = "\n".join(messages)

        with console.status("Thinking..."):
            result = populate_template(conversation)

        if result.completed:
            render_note(result)
            console.print("\n[bold green]Note complete![/bold green]")
            break

        questions = "\n".join(f"  • {q}" for q in result.questions)
        console.print(
            Text.from_markup(f"\n[bold cyan]Assistant:[/bold cyan]\n{questions}")
        )
        messages.append(f"Assistant: {questions}")


if __name__ == "__main__":
    main()
