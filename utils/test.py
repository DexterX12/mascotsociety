"""Convenience script to inspect a `.nofil` profile dump."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Iterable, Sequence

if __package__ in (None, ""):
	package_root = Path(__file__).resolve().parent.parent
	if str(package_root) not in sys.path:
		sys.path.insert(0, str(package_root))
	from utils.profile_handler import ProfileHandler
else:
	from .profile_handler import ProfileHandler


def format_collection_preview(items: Iterable[object], limit: int = 10) -> str:
	sequence: Sequence[object] = items if isinstance(items, Sequence) else list(items)
	head = [str(item) for item in sequence[:limit]]
	remaining = len(sequence) - len(head)
	if remaining > 0:
		head.append(f"... (+{remaining} more)")
	return "\n".join(head)


def main() -> None:
	parser = argparse.ArgumentParser(description="Inspect a serialized profile (.nofil file).")
	parser.add_argument(
		"profile",
		nargs="?",
		default="blank.nofil",
		help="Path to the .nofil file to load (default: %(default)s)",
	)
	parser.add_argument(
		"--show-friends",
		action="store_true",
		help="Print the full friend list after loading.",
	)
	parser.add_argument(
		"--show-items",
		action="store_true",
		help="Print the owned item list after loading.",
	)
	args = parser.parse_args()

	handler = ProfileHandler()

	try:
		handler.load_from_file(args.profile)
	except FileNotFoundError:
		raise SystemExit(f"Profile file not found: {args.profile}")

	source = Path(args.profile)
	print(f"\nLoaded profile from: {source.resolve() if source.exists() else args.profile}")
	print(f"Cash: {handler.cash}")
	print(f"Save number: {handler.save_number}")

	if handler.new_house_data:
		print(f"House data: {handler.new_house_data}")

	user = handler.user
	if user is None:
		print("No user data present in file.")
	else:
		print(f"User: {user.usernameFull or user.usernameShort or '<unknown>'}")
		if user.id:
			print(f"User ID: {user.id}")
		print(f"Credits: {user.credits}")
		print(f"Pet points: {user.petPoints} (level {user.petLevel})")
		total_items = len(user.ownedItems or [])
		print(f"Owned items: {total_items}")
		if args.show_items and user.ownedItems:
			print("\nOwned Items Preview:")
			print(format_collection_preview(user.ownedItems))

	print(f"Friends: {len(handler.friends)}")
	if args.show_friends and handler.friends:
		print("\nFriend List:")
		print(format_collection_preview(handler.friends))


if __name__ == "__main__":
	main()
