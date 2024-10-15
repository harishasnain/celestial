import pyplate

def solve_plate(image_path):
    # Initialize pyplate solver
    solver = pyplate.Solver()

    # Solve the plate
    result = solver.solve(image_path)

    if result.success:
        return {
            'ra': result.ra,
            'dec': result.dec,
            'rotation': result.rotation,
            'scale': result.scale,
            'stars': result.stars
        }
    else:
        raise ValueError("Failed to solve plate")