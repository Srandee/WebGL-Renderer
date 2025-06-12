import math
import itertools
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'Models', '4D')
os.makedirs(OUT_DIR, exist_ok=True)

# Utility to write obj file
def write_obj(path, vertices, faces):
    with open(path, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        for face in faces:
            if len(face) == 3:
                f.write(f"f {face[0]} {face[1]} {face[2]}\n")
            elif len(face) == 4:
                f.write(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")

# Perspective project from 4D to 3D
def proj(p):
    x,y,z,w = p
    scale = 1.0/(2.0 - w)
    return (x*scale, y*scale, z*scale)

def generate_tesseract():
    verts4 = list(itertools.product([-1,1], repeat=4))
    verts = [proj(v) for v in verts4]
    idx = {v:i for i,v in enumerate(verts4)}
    faces = []
    dims = [0,1,2,3]
    for i in range(4):
        for j in range(i+1,4):
            other = [d for d in dims if d not in (i,j)]
            for signs in itertools.product([-1,1], repeat=2):
                base = [0,0,0,0]
                base[other[0]] = signs[0]
                base[other[1]] = signs[1]
                square = []
                for pair in [(-1,-1),(1,-1),(1,1),(-1,1)]:
                    p = list(base)
                    p[i] = pair[0]
                    p[j] = pair[1]
                    square.append(idx[tuple(p)]+1)
                faces.append([square[0],square[1],square[2]])
                faces.append([square[0],square[2],square[3]])
    write_obj(os.path.join(OUT_DIR,'tesseract.obj'), verts, faces)

def generate_5cell():
    s = math.sqrt(1/10)
    verts4 = [
        (1,1,1,-1),
        (1,-1,-1,-1),
        (-1,1,-1,-1),
        (-1,-1,1,-1),
        (0,0,0,3)
    ]
    verts4 = [(x*s,y*s,z*s,w*s) for x,y,z,w in verts4]
    verts = [proj(v) for v in verts4]
    faces = []
    for a,b,c in itertools.combinations(range(5),3):
        faces.append([a+1,b+1,c+1])
    write_obj(os.path.join(OUT_DIR,'5cell.obj'), verts, faces)

def generate_pseudosphere(res_u=32,res_v=16):
    verts = []
    faces = []
    for i in range(res_v+1):
        v = i/(res_v)*math.pi/2 - 0.0001
        for j in range(res_u):
            u = j/res_u*2*math.pi
            x = math.cos(u)*math.sin(v)
            y = math.sin(u)*math.sin(v)
            z = math.cos(v) + math.log(math.tan(v/2+math.pi/4))
            verts.append((x,y,z))
    for i in range(res_v):
        for j in range(res_u):
            p0 = i*res_u + j
            p1 = i*res_u + (j+1)%res_u
            p2 = (i+1)*res_u + (j+1)%res_u
            p3 = (i+1)*res_u + j
            faces.append([p0+1,p1+1,p2+1])
            faces.append([p0+1,p2+1,p3+1])
    write_obj(os.path.join(OUT_DIR,'pseudosphere.obj'), verts, faces)

if __name__ == '__main__':
    generate_tesseract()
    generate_5cell()
    generate_pseudosphere()
