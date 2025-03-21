import jwt from 'jsonwebtoken'

const verifyToken = (req, res, next) => {
    const authorizationHeader = req.headers['authorization']
    if (!authorizationHeader) return res.status(401).json({message: '401 Unauthorized'})

    const token = authorizationHeader.split('Bearer ')[1]
    if (!token) return res.status(401).json({message: '401 Unauthorized'})

    jwt.verify(token, process.env.JWT_ACCESS_TOKEN_SECRET, async (err, data) => {
        if (err) return res.status(403).json({message: '403 Forbidden'})
        req.user = data;
        next();
    })
}

const verifyTokenSocket = (socket, next) => {
    const token = socket.handshake.auth.token;
    if (!token) {
        return next(new Error('401 Unauthorized'));
    }

    jwt.verify(token, process.env.JWT_ACCESS_TOKEN_SECRET, (err, data) => {
        if (err) {
            return next(new Error('403 Forbidden'));
        }
        socket.user = data;  // Attach the decoded user data to the socket object
        next();  // Proceed with the connection
    });
};

export {
    verifyToken,
    verifyTokenSocket
}
