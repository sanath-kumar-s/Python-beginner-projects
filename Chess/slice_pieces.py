import os
from PIL import Image

def slice_chess_pieces(sheet_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(sheet_path).convert("RGBA")
    width, height = img.size
    
    # Grid info
    rows = 2
    cols = 6
    piece_w = width // cols
    piece_h = height // rows

    # Piece names in order of the sheet
    # Row 1: King, Queen, Rook, Bishop, Knight, Pawn (White)
    # Row 2: King, Queen, Rook, Bishop, Knight, Pawn (Black)
    names = [
        ["wK", "wQ", "wR", "wB", "wN", "wP"],
        ["bK", "bQ", "bR", "bB", "bN", "bP"]
    ]

    for r in range(rows):
        for c in range(cols):
            left = c * piece_w
            top = r * piece_h
            right = left + piece_w
            bottom = top + piece_h
            
            piece = img.crop((left, top, right, bottom))
            
            # Make background transparent (white threshold)
            datas = piece.getdata()
            new_data = []
            for item in datas:
                # If pixel is very close to white, make it transparent
                if item[0] > 245 and item[1] > 245 and item[2] > 245:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            
            piece.putdata(new_data)
            
            # Trim margins (optional but recommended for better centring)
            # Find bounding box of non-transparent pixels
            bbox = piece.getbbox()
            if bbox:
                piece = piece.crop(bbox)
            
            # Pad back to square if needed or just save as is
            # For chess, square pieces are easier. Let's make it 200x200 or similar.
            max_dim = max(piece.size)
            square_piece = Image.new("RGBA", (max_dim, max_dim), (255, 255, 255, 0))
            offset = ((max_dim - piece.width) // 2, (max_dim - piece.height) // 2)
            square_piece.paste(piece, offset)
            
            name = names[r][c]
            square_piece.save(os.path.join(output_dir, f"{name}.png"))
            print(f"Saved {name}.png")

if __name__ == "__main__":
    sheet = r"C:\Users\Anjana Enterprises\.gemini\antigravity\brain\160481fb-5ae1-4929-88f4-797fdfa9082e\chess_pieces_sheet_1777013209889.png"
    out = r"c:\Users\Anjana Enterprises\OneDrive\Pictures\Chess\assets\images\pieces"
    slice_chess_pieces(sheet, out)
