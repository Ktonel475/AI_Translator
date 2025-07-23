import argparse
import os
from Agent.translator import Translator
from yaspin import yaspin

def main():
    parser = argparse.ArgumentParser(description="Translate article using AI")
    parser.add_argument("file", help="Path to the markdown/text file")
    parser.add_argument("-s", "--src", help="Source language (optional)", default=None)
    parser.add_argument("-t", "--target", help="Target language", required=True)
    parser.add_argument("-o", "--output-dir", help="Directory to save the translated file", default=None)

    args = parser.parse_args()

    # Load file content
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {args.file}")
        return

    # Create translator instance
    translator = Translator()

    # Show spinner while translating
    with yaspin(text="Translating...", color="cyan") as spinner:
        try:
            translated = translator.translate(
                text=content,
                src_lang=args.src,
                target_lang=args.target
            )
            spinner.ok("✓")
        except Exception as e:
            spinner.fail("💥")
            print(f"Translation failed: {e}")
            return
        
    print("\n=== Translated Output ===\n")
    print(translated)
    
    input_filename = os.path.basename(args.file)
    name, ext = os.path.splitext(input_filename)
    output_filename = f"{name}_translated{ext}"

    # Determine output path
    output_dir = args.output_dir or os.path.dirname(args.file)
    output_path = os.path.join(output_dir, output_filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save result
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(translated)

    print(f"\n✅ Translation completed and saved to: {output_path}")
    

if __name__ == "__main__":
    main()
