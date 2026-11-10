import argparse
from datetime import datetime, timezone

from daneel.detection import Transit
from daneel.parameters import Parameters


def main():
    parser = argparse.ArgumentParser(description="Model and analyse exoplanet transits.")

    parser.add_argument(
        "-i",
        "--input",
        dest="input_file",
        type=str,
        required=True,
        help="Input par file to pass",
    )

    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-t", "--transit", action="store_true", help="Plot a transit light curve")

    actions.add_argument("-d", "--detect", action="store_true", help="Run exoplanet detection")
    actions.add_argument("-a", "--atmosphere", action="store_true", help="Run atmospheric characterisation")
    parser.add_argument("-o", "--output", default="lc.png", help="Output image for --transit")
    parser.add_argument("-r", "--radii", default=1, help="Plot multiple radii")

    args = parser.parse_args()

    """Launch Daneel"""
    start = datetime.now(timezone.utc)

    input_pars = Parameters(args.input_file).params

    try:
        args.radii = int(args.radii)
    except:
        args.radii = 1
        print('Please enter integer number of radii, defaulting to 1...')

    if args.transit:
        transit = Transit(input_pars['transit'])
        if args.radii != 1:
            transit.plot_multi_light_curve(args.output, args.radii)
        else:
            transit.plot_light_curve(args.output)
    elif args.detect:
        parser.error("detection is not implemented yet; use --transit")
    elif args.atmosphere:
        parser.error("atmospheric characterisation is not implemented yet; use --transit")

    finish = datetime.now(timezone.utc)
    print(f"Daneel completed in {(finish - start).total_seconds():.2f}s")
    # print('Current time: ' + str(finish)) # For debugging, to make sure editing correct file

if __name__ == "__main__":
    main()
