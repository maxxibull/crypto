import argparse

def main(args):
    output = "".join([str(ord(a) ^ ord(b)) for a,b in zip(args.iv_previous,args.iv_new)])
    with open(args.output_path, mode="w") as output_file:
        output_file.write(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iv-previous", required=True, help="Previous nitial vector")
    parser.add_argument("--iv-new", required=True, help="New initial vector")
    parser.add_argument("--output-path", required=True, help="Path to output file")
    args = parser.parse_args()
    main(args)
