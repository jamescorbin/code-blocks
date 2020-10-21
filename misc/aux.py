import numpy as np

###############################################################################

###############################################################################

def span_orthogonal(u, eps=1e-4, unit_vects=None):
    '''
    parameters:
            -- ${u}, a (numpy) vector of dimension ${dim}
            -- ${eps}, numerical error
            -- ${unit_vects}, array of dimension ${dim}x${dim}.
                        supersedes the diagonal matrix for
                        test basis in Gram-Schmidt.
                        With proper selection of ${unit_vects}
                        this would allow a continuous frame
                        if ${u} varies continously.
    returns:
            --${ortho}, a matrix of shape ${dim}x${dim}
                        consisting of ${u} in the first row
                        and remaining rows form orthogonal basis
                        of the hyperplane orthogonal to ${u}.
    '''
    if np.abs(np.dot(u, u)-1) > eps:
        u = u/np.sqrt(np.dot(u, u))
    try:
        assert ~np.isnan(u).any(), "Input is zero vector or has nan."
    except AssertionError as error:
        print(error)
    dim = u.shape[0]
    if unit_vects is None:
        unit_vects = np.diagflat(np.ones(dim))

    ortho = np.zeros((dim, dim))
    ortho[0, :] = u
    ind1 = 1
    ind2 = 1
    while ind2 < dim:
        if ind1 == dim:
            ind1 = 0
        check = all([
                np.abs(
                np.dot(ortho[j], unit_vects[ind1])**2
                - 1) > eps
                for j in range(ind2)
                ])
        if check:
            ortho[ind2, :] = (unit_vects[ind1]
                    - np.sum(np.array([
                    np.dot(ortho[j, :], unit_vects[ind1])
                    * ortho[j, :] for j in range(ind2)]),
                    axis=0)
                    )
            ortho[ind2, :] = (ortho[ind2, :]
                    / np.sqrt(
                    np.dot(ortho[ind2, :], ortho[ind2, :])))
            if (np.sum((ortho[ind2] - unit_vects[ind1])**2)
                    > np.sum((ortho[ind2] + unit_vects[ind1])**2)):
                ortho[ind2, :] = -ortho[ind2, :]
            ind2 += 1
            ind1 += 1
        else:
            ind1 += 1

    if dim == 3:
        if np.dot(np.cross(ortho[0, :], ortho[1, :]), ortho[2, :]) < 0:
            ortho[2, :] = -ortho[2, :]
    return ortho

###############################################################################

###############################################################################

def direction_angles(U, v):
    '''
    '''
    A = np.matmul(U, v)
    assert np.abs(A[1]) <= 1, str(A[1])
    assert np.abs(A[2]) <= 1, str(A[2])
    return A, (np.arccos(A[1]) - np.pi/2), (np.arccos(A[2]) - np.pi/2)

###############################################################################

###############################################################################

def rodriguez_formula(k, v, th):
    '''
    '''
    K = np.array([
        [0, -k[2], k[1]],
        [k[2], 0, -k[0]],
        [-k[1], k[0], 0]
        ])
    ret =  (v + np.sin(th) * np.matmul(K, v)
            + (1 - np.cos(th)) * np.matmul(K, np.matmul(K, v)))
    return ret / np.sqrt(np.dot(ret, ret))

###############################################################################

###############################################################################

def increment_direction(v, th2, th3):
    '''
    description:
            The vector ${v} is upto a small
            deviation aligned with the ${x_1}-axis.

    '''
    U = span_orthogonal(v)
    q = rodriguez_formula(U[1], v, th3)
    return rodriguez_formula(U[2], q, -th2)

###############################################################################
