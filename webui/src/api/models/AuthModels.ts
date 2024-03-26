export type AuthRequest = {
    username: string;
    password: string;
};

export type AuthResponse = {
    username: string;
    access_token: string;
    msg: string;
};
