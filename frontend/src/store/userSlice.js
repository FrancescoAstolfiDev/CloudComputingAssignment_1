import { createSlice } from '@reduxjs/toolkit';

export const userSlice = createSlice({
    name: 'user',
    initialState: {
        userId: null
    },
    reducers: {
        setUserId: (state, action) => {
            state.userId = action.payload;
        },
        clearUserId: (state) => {
            state.userId = null;
        }
    }
});

// Export delle azioni
export const { setUserId, clearUserId } = userSlice.actions;

// Export del reducer
export default userSlice.reducer;
